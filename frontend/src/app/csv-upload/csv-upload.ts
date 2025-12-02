import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

interface UploadResponse {
  success: boolean;
  imported: number;
  not_imported: number;
  errors: {
    line?: number;
    contract_number?: string;
    error: string;
  }[];
}

@Component({
  selector: 'app-csv-upload',
  imports: [CommonModule],
  standalone: true,
  templateUrl: './csv-upload.html',
  styleUrl: './csv-upload.css',
})
export class CsvUpload {
  selectedFile: File | null = null;
  status: 'idle' | 'selected' | 'uploading' | 'success' | 'error' = 'idle';
  errorMessage = '';
  importedCount: number | null = null;
  notImportedCount: number | null = null;
  backendErrors: UploadResponse['errors'] | null = null;
  /** Start Time of an upload in ms */
  uploadStartTime: number | null = null;
  /** Duration Time converted later on in onUpload() into seconds  */
  uploadDuration: number | null = null;

  private readonly requestUrl = 'http://localhost:8000/contracts/upload';

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
    this.notImportedCount = null;
    this.backendErrors = null;
  }

  onUpload() {
    if (!this.selectedFile) {
      return;
    }

    this.status = 'uploading';
    this.errorMessage = '';
    this.importedCount = null;
    this.notImportedCount = null;
    this.backendErrors = null;
    this.uploadStartTime = Date.now();
    this.uploadDuration = null;

    const formData = new FormData();
    formData.append('file', this.selectedFile);

    this.http.post<UploadResponse>(this.requestUrl, formData).subscribe({
      next: (res) => {
        if (this.uploadStartTime) {
          this.uploadDuration = (Date.now() - this.uploadStartTime) / 1000;
        }
        if (res.success) {
          this.status = 'success';
          this.importedCount = res.imported;
        } else {
          this.status = 'error';
          this.backendErrors = res.errors;
          this.errorMessage = 'Fehler beim Import';
          this.importedCount = res.imported;
          this.notImportedCount = res.not_imported;
          console.log('Imported: ', res.imported);
          console.log('Not Imported: ', res.not_imported);
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
