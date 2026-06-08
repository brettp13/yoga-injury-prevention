import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { ContactService } from './contact.component.service';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.css']
})
export class ContactComponent implements OnInit {
  contactForm: FormGroup;
  contactSuccess = false;

  constructor(private contactService: ContactService) { }

  ngOnInit() {
    this.contactForm = new FormGroup({
      'fullName': new FormControl(null, [Validators.required]),
      'email': new FormControl(null, [Validators.required, Validators.email]),
      'message': new FormControl(null, [Validators.required])
    });
    this.toTop();
  }

  // shortcut functions
  get fullName() {return this.contactForm.get('fullName')};
  get email() {return this.contactForm.get('email')};
  get message() {return this.contactForm.get('message')};

  onSubmit() {
    this.contactService.createContactMessage(
      [
        {
          'full_name': this.fullName.value,
          'email': this.email.value,
          'message': this.message.value
        }
      ])
        .subscribe(
          (response) => { 
            console.log(response);

            this.contactSuccess = true;
            this.contactForm.reset();
            
            // Dismiss 'thank you' alert after 3 seconds
            setTimeout(() => {
              this.contactSuccess = false;
            }, 3000);
          },
          (error) => console.log(error)
        );
  }

  toTop() {
    document.body.scrollTop = document.documentElement.scrollTop = 0;
  }

}
