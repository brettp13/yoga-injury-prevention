import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { Router } from '@angular/router';

import { UserService } from '../shared/user.service';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
  @ViewChild('closeModal') closeModal: ElementRef;
  userSignedIn: boolean;
  modalIsOpen: boolean = false;

  constructor(private userService: UserService,
              private router: Router) { }

  logOut() {
    this.userService.signedOut();
    this.router.navigate([''])
  }

  openModal() {
    this.modalIsOpen = true;
  }

  exitModal() {
    this.modalIsOpen = false;
  }

  ngOnInit() {
    this.userService.userSignedIn.subscribe(
      (value) => {
        if (value === true && this.modalIsOpen) {
          this.closeModal.nativeElement.click();
          this.exitModal();
        }
        this.userSignedIn = value;
    });
  }
}
