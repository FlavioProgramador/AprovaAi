import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  isLogin = true;
  email = '';
  password = '';
  confirmPassword = '';
  errorMsg = '';
  loading = false;

  constructor(private authService: AuthService, private router: Router) {
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/']);
    }
  }

  toggleMode(): void {
    this.isLogin = !this.isLogin;
    this.errorMsg = '';
    this.email = '';
    this.password = '';
    this.confirmPassword = '';
  }

  onSubmit(): void {
    if (!this.email || !this.password) {
      this.errorMsg = 'Por favor, preencha todos os campos.';
      return;
    }

    if (!this.isLogin && this.password !== this.confirmPassword) {
      this.errorMsg = 'As senhas não coincidem.';
      return;
    }

    this.loading = true;
    this.errorMsg = '';

    if (this.isLogin) {
      this.authService.login(this.email, this.password).subscribe({
        next: () => {
          this.loading = false;
          this.router.navigate(['/']);
        },
        error: (err) => {
          this.loading = false;
          this.errorMsg = err.error?.detail || 'Erro ao realizar login. Verifique suas credenciais.';
        }
      });
    } else {
      this.authService.register(this.email, this.password).subscribe({
        next: () => {
          this.authService.login(this.email, this.password).subscribe({
            next: () => {
              this.loading = false;
              this.router.navigate(['/']);
            },
            error: () => {
              this.loading = false;
              this.isLogin = true;
              this.errorMsg = 'Cadastro realizado com sucesso! Faça login.';
            }
          });
        },
        error: (err) => {
          this.loading = false;
          this.errorMsg = err.error?.detail || 'Erro ao cadastrar usuário. Tente outro e-mail.';
        }
      });
    }
  }
}
