import { Component, 
         OnInit,  
         ViewChild, 
         ElementRef,
         ChangeDetectorRef
       } from '@angular/core';

import { FormGroup, FormControl, Validators } from '@angular/forms';

import { SignupService } from '../shared/signup.service';
import { EmailIsTakenValidator } from './email.validator';
import { EmailValidationService } from '../shared/email-validation.service';
import { UserService } from '../shared/user.service';
import { YogaPoseService } from '../shared/yogapose.service';


declare var Stripe: any;

@Component({
  selector: 'app-join-form',
  templateUrl: './join-form.component.html',
  styleUrls: ['./join-form.component.css']
})
export class JoinFormComponent implements OnInit {
  signUpForm: FormGroup;
  token: string;
  signUpFormErrorMessage: any;
  yogaStyles: any;
  currentStep: number = 0;
  defaultOption = null;

  // Stuff for Stripe
  stripe: any;
  elements: any;
  card: any;
  cardHandler = this.onChange.bind(this);
  error: string;
  stripe_token: string; 
  @ViewChild('cardElement') cardInfo: ElementRef;

  // Traffic source
  trafficSource: string = '';

  constructor(private signUpService: SignupService,
              private emailValidationService: EmailValidationService,
              private userService: UserService,
              private yogaPoseService: YogaPoseService,
              private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    // configure form
    this.signUpForm = new FormGroup({
      'firstName': new FormControl(null, [Validators.required]),
      'lastName': new FormControl(null, [Validators.required]),
      'email': new FormControl(
        null, 
        [Validators.required, Validators.email], 
        EmailIsTakenValidator.createValidator(this.emailValidationService)
      ),
      'isTeacher': new FormControl(null),
      'yogaStyle': new FormControl(null),
    });
    // Add the password and verifyPassword controls separately so we can use our 
    // custom validator
    this.signUpForm.addControl('password', new FormControl('', Validators.required));
    this.signUpForm.addControl('verifyPassword', new FormControl(
      '', [Validators.compose(
        [Validators.required, this.validateAreEqual.bind(this)]
      )]
    ))

    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });

    this.signUpService.signUpErrors.subscribe(
      (signUpErrors) => {
        this.signUpFormErrorMessage = signUpErrors;
      });

    this.signUpService.stripeToken.subscribe(
      (stripeToken) => {
        this.stripe_token = stripeToken;
      }
    )

    this.yogaPoseService.yogaStyles.subscribe(
      (yogaStyles) => {
        this.yogaStyles = yogaStyles;
      });
  
    this.yogaPoseService.getYogaStyles();
  }

  changeForm(step: string) {
    this.currentStep = step === 'prev' ? this.currentStep -1 : this.currentStep + 1;
    if (this.currentStep === 4) {

      this.cdr.detectChanges();

      //this.stripe = Stripe("pk_test_cfE9dndAoZGRxcXreTUBWdVJ");
      this.stripe = Stripe('pk_live_m4Gdciog99LDC4icu4GM6u36');
      this.elements = this.stripe.elements();
      const style = {
             base: {
               fontSize: '16px',
               color: '#32325d',
             },
           };
           this.card = this.elements.create('card', {
             style
           });
           this.card.mount(this.cardInfo.nativeElement);
           this.card.addEventListener('change', this.cardHandler);
    }
  }

  onChange({
    error
  }) {
    if (error) {
        this.error = error.message;
    } else {
        this.error = null;
    }
    this.cdr.detectChanges();
}

private validateAreEqual(fieldControl: FormControl) {
  if (fieldControl.value === "") {
      return fieldControl.value === this.signUpForm.get("password").value ? null : {
        passwordsMustMatch: false
      };
  } else {
    return fieldControl.value === this.signUpForm.get("password").value ? null : {
      passwordsMustMatch: true
    };
  }
}
  // shortcut functions
  get firstName() {return this.signUpForm.get('firstName')};
  get lastName() {return this.signUpForm.get('lastName')};
  get email() {return this.signUpForm.get('email')};
  get password() {return this.signUpForm.get('password')};
  get verifyPassword() {return this.signUpForm.get('verifyPassword')};
  get isTeacher() {return this.signUpForm.get('isTeacher')};
  get yogaStyle() {return this.signUpForm.get('yogaStyle')};

  async getToken() {
    const { token, error } = await this.stripe.createToken(this.card);
    if (error) {
      console.log('Something is wrong:', error);
    } else {
      this.stripe_token = token.id

      const trafficSource = localStorage.getItem('trafficSource');
      if (trafficSource) {
        this.trafficSource = trafficSource;
      } else {
        this.trafficSource = 'organic';
      }

      this.signUpService.createSignUp([
        {
          'first_name': this.firstName.value,
          'last_name': this.lastName.value,
          'email': this.email.value,
          'password': this.password.value,
          'is_teacher': this.isTeacher.value,
          'yoga_style': this.yogaStyle.value,
          'token': this.stripe_token,
          'traffic_source': this.trafficSource
        }
      ]);
    }
  }

  onSubmit() {
    this.getToken();
  }
}
