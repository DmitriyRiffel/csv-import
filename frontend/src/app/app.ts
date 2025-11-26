import { Component, signal } from '@angular/core';
import { CsvUpload } from './csv-upload/csv-upload';

@Component({
  selector: 'app-root',
  imports: [CsvUpload],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('frontend');
}
