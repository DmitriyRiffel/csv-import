import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

interface UploadResponse {
  success: boolean;
  imported: number;
  errors: {
    line: number;
    error: string;
    raw: Record<string, string>;
  }[];
}

@Component({
  selector: 'app-csv-upload',
  imports: [CommonModule],
  templateUrl: './csv-upload.html',
  styleUrl: './csv-upload.css',
})
export class CsvUpload {
  selectedFile: File | null = null;
  status: 'idle' | 'selected' | 'uploading' | 'success' | 'error' = 'idle';
  errorMessage = '';
  importedCount: number | null = null;
  backendErrors: UploadResponse['errors'] | null = null;

  private readonly uploadUrl = 'http://localhost:8000/contracts/upload';

  constructor(private http: HttpClient) {}

  onFileSelected(event: Event) {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0] ?? null;

    if (!file) {
      this.selectedFile = null;
      this.status = 'idle';
      return;
    }

    this.selectedFile = file;
    this.status = 'selected';
    this.errorMessage = '';
    this.importedCount = null;
    this.backendErrors = null;
  }

  onUpload() {
    if (!this.selectedFile) {
      return;
    }

    this.status = 'uploading';
    this.errorMessage = '';
    this.importedCount = null;
    this.backendErrors = null;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<UploadResponse>(this.uploadUrl, formData).subscribe({
      next: (res) => {
        if (res.success) {
          this.status = 'success';
          this.importedCount = res.imported;
        } else {
          this.status = 'error';
          this.backendErrors = res.errors;
          this.errorMessage = 'Fehler beim Import';
        }
      },
      error: (err) => {
        this.status = 'error';
        this.errorMessage =
          err.error?.detail ?? 'Unbekannter Fehler beim Upload';
      },
    });
  }
}
