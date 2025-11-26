import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';

interface Contract {
  contract_number: string;
  start_date: string;
  end_date: string | null;
  status: string;
}

@Component({
  selector: 'app-contracts-table',
  imports: [],
  templateUrl: './contracts-table.html',
  styleUrl: './contracts-table.css',
})
export class ContractsTable {
  private readonly requestUrl = 'http://localhost:8000/contracts';
  constructor(private http: HttpClient) {}
  contracts: Contract[] = [];
  loading = false;
  errorMessage = '';
  ngOnInit(): void {
    this.getAllContracts();
  }

  getAllContracts() {
    this.loading = true;
    this.errorMessage = '';
    this.http.get<Contract[]>(this.requestUrl).subscribe({
      next: (data) => {
        this.contracts = data;
        this.loading = false;
      },
      error: (error) => {
        console.error(error);
        this.errorMessage = 'Fehler beim Laden der Verträge';
        this.loading = false;
      },
    });
  }
}
