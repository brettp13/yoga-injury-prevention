import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

import { ConditionsService } from '../../shared/conditions.service';
import { UserService } from '../../shared/user.service';
import { VideoService } from 'src/app/shared/video.service';
import { YogaPoseService } from '../../shared/yogapose.service'; 

@Component({
  selector: 'app-view-condition',
  templateUrl: './view-condition.component.html',
  styleUrls: ['./view-condition.component.css']
})
export class ViewConditionComponent implements OnInit {
  condition: any;
  beneficialPoses: any;
  contraindicatedPoses: any;
  safePoses: any;
  howYogaHelps: any;
  token: string;

  constructor(private conditionsService: ConditionsService,
              private userService: UserService,
              private yogaPoseService: YogaPoseService,
              private router: Router,
              private videoService: VideoService,
              private location: Location) { }

  ngOnInit() {
    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });

    this.conditionsService.selectedCondition.subscribe(
      (selectedCondition) => {
        this.condition = selectedCondition;
        // once subscription returns, use condition id to get 
        // everything else
        this.conditionsService.getHowYogaHelps(this.token, this.condition.id);
        this.conditionsService.searchByConditionBeneficial(this.token, [this.condition.id]);
        this.conditionsService.searchByConditionContraindicated(this.token, [this.condition.id]);
      });
    
    this.conditionsService.beneficialConditionSearchResults.subscribe(
      (beneficialPoses) => {
        this.beneficialPoses = beneficialPoses;
      });

    this.conditionsService.contraindicatedConditionSearchResults.subscribe(
      (contraindicatedPoses) => {
        this.contraindicatedPoses = contraindicatedPoses;
      });

    this.conditionsService.safeConditionSearchResults.subscribe(
      (safePoses) => {
        this.safePoses = safePoses;
      });

    this.conditionsService.howYogaHelps.subscribe(
      (howYogaHelps) => {
        this.howYogaHelps = howYogaHelps;
      });
  }

  back() {
    this.location.back();
  }

  viewPose(id: number) {
    this.yogaPoseService.selectPose(this.token, id);
    this.yogaPoseService.getConditionsContraindicatedByPose(id, this.token);
    this.yogaPoseService.getConditionsHelpedByPose(id, this.token);
    this.yogaPoseService.cameFrom.next('conditions');
    this.router.navigate(['dashboard', 'pose-view']);
  }

  viewVideo(pose_video: string) {
    this.videoService.videoUrl.next(pose_video);
    this.router.navigate(['dashboard', 'view-video']);
  }
}
