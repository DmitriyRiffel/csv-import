import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

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
  }

  onUpload() {
    if (!this.selectedFile) {
      return;
    }

    this.status = 'uploading';
    this.errorMessage = '';

    //ToDo: integrate backend endpoint for upload a file
    setTimeout(() => {
      this.status = 'success';
    }, 1000);
  }
}
