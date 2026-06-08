import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

import { ConditionsService } from '../../shared/conditions.service';
import { UserService } from '../../shared/user.service';
import { YogaPoseService } from '../../shared/yogapose.service';

@Component({
  selector: 'app-view-pose',
  templateUrl: './view-pose.component.html',
  styleUrls: ['./view-pose.component.css']
})
export class ViewPoseComponent implements OnInit {
  token: string;
  selectedPose: any;
  contraindicatedConditions: any;
  indicatedConditions: any;
  cameFrom: String;

  constructor(private router: Router,
              private location: Location,
              private conditionsService: ConditionsService,
              private userService: UserService,
              private yogaPoseService: YogaPoseService) { }

  ngOnInit() {
    this.yogaPoseService.selectedPose.subscribe(
      (selectedPose) => {
        this.selectedPose = selectedPose;
      });

    this.yogaPoseService.conditionsContraindicated.subscribe(
      (contraindicatedConditions) => {
        this.contraindicatedConditions = contraindicatedConditions;
      });

    this.yogaPoseService.conditionsHelped.subscribe(
      (helpedConditions) => {
        this.indicatedConditions = helpedConditions;
      });

    this.yogaPoseService.cameFrom.subscribe(
      (cameFrom) => {
        this.cameFrom = cameFrom;
      });

    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });
  }

  returnToPoses() {
    this.router.navigate(['dashboard', 'search-by-pose']);
  }

  returnToConditions() {
    this.location.back();
  }

  viewCondition(id: number) {
    this.conditionsService.selectCondition(this.token, id);
    this.router.navigate(['dashboard', 'view-condition']);
  }

}
