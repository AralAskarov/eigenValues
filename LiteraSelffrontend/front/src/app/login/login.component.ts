import { Component, OnInit } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {BooksService } from '../books.service';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive, FormsModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})

export class LoginComponent implements OnInit {
  title:string = 'Connection to Django app';
  logged: boolean = false;
  username: string = "";
  password: string = "";

  
  constructor(private booksService: BooksService, private router: Router){

  }

  ngOnInit() : void {
    const access: string|null = localStorage.getItem("access");
    if(access){
      this.logged = true;
    }
  }

  login() : void {
    this.booksService.login(this.username, this.password).subscribe((data) => {
      this.logged = true;
      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      this.router.navigate(['/profile']);

    })


  }

  logout(): void {
    this.logged = false;
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
  }



}
