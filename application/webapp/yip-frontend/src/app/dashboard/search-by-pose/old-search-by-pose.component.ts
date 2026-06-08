import { Component, OnInit } from '@angular/core';

import { UserService } from '../../shared/user.service';
import { YogaPoseService } from '../../shared/yogapose.service';

@Component({
  selector: 'app-search-by-pose',
  templateUrl: './search-by-pose.component.html',
  styleUrls: ['./search-by-pose.component.css', './slider.css']
})
export class SearchByPoseComponent implements OnInit {
  token: string;
  poses: any;
  conditionsHelped: any;
  conditionsContraindicated: any;

  displayPoseSection = false;
  displayedPose: any;

  settings = {
    actions: false,
    columns: {
      english_name: {
        title: 'English name',
      },
      sanskrit_name: {
        title: 'Sanskrit name'
      }
    }
  };

  constructor(private userService: UserService,
              private yogaposeService: YogaPoseService) { }

  ngOnInit() {
    this.userService.token.subscribe(token => {
      this.token = token;
    });

    this.yogaposeService.listOfPoses.subscribe(
      newListOfPoses => {
        console.log('got a new list of poses!');
        this.poses = newListOfPoses;
      });

    this.yogaposeService.conditionsHelped.subscribe(
      newConditionsHelped => {
        console.log('got a new list of conditions helped');
        this.conditionsHelped = newConditionsHelped;
      });

    this.yogaposeService.conditionsContraindicated.subscribe(
      newConditionsContraindicated => {
        console.log('Got a new list of conditions contraindicated');
        this.conditionsContraindicated = newConditionsContraindicated;
      });

    this.yogaposeService.getPoses(this.token);
  }
  
  onUserRowSelect(event): void {
    console.log('Called row select');
    this.displayPoseSection = true;
    this.displayedPose = event.data;
    this.yogaposeService.getConditionsHelpedByPose(event.data.id, this.token);
    this.yogaposeService.getConditionsContraindicatedByPose(event.data.id, this.token);
  }
}
