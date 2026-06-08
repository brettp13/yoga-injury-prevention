import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl, Validators } from '@angular/forms';

import { UserService } from '../../shared/user.service';
import { ForgotPasswordService } from '../../shared/forgot-password.service';

@Component({
  selector: 'app-signin-form',
  templateUrl: './signin-form.component.html',
  styleUrls: ['./signin-form.component.css']
})
export class SigninFormComponent implements OnInit {
  signInForm: FormGroup;
  signInFormErrorMessage: string;
  forgotPasswordForm: boolean = false;
  newPasswordSentAlert: boolean = false;

  constructor(private userService: UserService,
              private forgotPasswordService: ForgotPasswordService) { }

  ngOnInit() {
    this.signInForm = new FormGroup({
      'email': new FormControl(null, [Validators.required, Validators.email]),
      'password': new FormControl(null, Validators.required)
    });

    this.userService.loginErrors.subscribe(
      (errorMessage) => {
        this.signInFormErrorMessage = errorMessage;
      });

    this.forgotPasswordService.forgotPasswordForm.subscribe(
      (showForm) => {
        this.forgotPasswordForm = showForm;
        this.signInFormErrorMessage = '';
      }
    )

    this.forgotPasswordService.newPasswordSentAlert.subscribe(
      (showAlert) => {
        this.newPasswordSentAlert = showAlert;
      }
    )
  }

  get email() {return this.signInForm.get('email')}
  get password() {return this.signInForm.get('password')}

  onSubmit() {
    this.userService.login(this.email.value, this.password.value);
  }

  forgotPassword() {
    this.forgotPasswordService.showForgotPasswordForm();
  }
}
