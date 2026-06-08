import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';


import { ConditionsService } from '../shared/conditions.service';
import { UserService } from '../shared/user.service';

@Component({
  selector: 'app-medical-glossary',
  templateUrl: './medical-glossary.component.html',
  styleUrls: ['./medical-glossary.component.css']
})
export class MedicalGlossaryComponent implements OnInit {

  conditionList = <any>[];
  token: string;

  constructor(private conditionService: ConditionsService,
              private userService: UserService,
              private router: Router) { }

  ngOnInit() {
    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });

    this.conditionService.listOfConditions.subscribe(
      (listOfConditions) => {
        this.conditionList = listOfConditions;
      });

    this.conditionService.getConditions(this.token);
  }

  viewCondition(condition_id: number) {
    this.conditionService.selectCondition(this.token, condition_id);
    this.router.navigate(['dashboard', 'view-condition']);
  }
}
