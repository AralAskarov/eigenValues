import { Component, OnInit } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import {BooksService } from '../books.service';
@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, RouterOutlet, RouterLink, RouterLinkActive, FormsModule],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent {
  logged: boolean = false;
  username: string = "";
  password: string = "";


  constructor(private booksService: BooksService,private router: Router){

  }

  ngOnInit() : void {
    const access: string|null = localStorage.getItem("access");
    if(access){
      this.logged = true;
    }
  }
  logout(): void {
    this.logged = false;
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    this.router.navigate(['']);

  }
}
