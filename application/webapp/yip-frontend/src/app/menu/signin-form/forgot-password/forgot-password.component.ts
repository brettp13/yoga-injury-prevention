import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { ForgotPasswordService } from '../../../shared/forgot-password.service';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.component.html',
  styleUrls: ['./forgot-password.component.css']
})
export class ForgotPasswordComponent implements OnInit {
  forgotPasswordForm: FormGroup;
  forgotPasswordFormErrorMessage: string = '';

  constructor(private forgotPasswordService: ForgotPasswordService) { }

  ngOnInit() {
    this.forgotPasswordForm = new FormGroup({
      'forgotPasswordEmail': new FormControl(null, [Validators.required, Validators.email])
    });
  }

  get forgotPasswordEmail() {return this.forgotPasswordForm.get('forgotPasswordEmail')};

  submitForgotPasswordForm() {
    this.forgotPasswordService.resetPassword(this.forgotPasswordEmail.value);
    this.forgotPasswordForm.reset();
    this.forgotPasswordService.hideForgotPasswordForm();
    this.forgotPasswordService.showPasswordSentAlert();
    
  }
}
