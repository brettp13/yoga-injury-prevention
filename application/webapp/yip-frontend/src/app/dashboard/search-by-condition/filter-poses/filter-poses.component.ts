import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ConditionsService } from 'src/app/shared/conditions.service';
import { FilterPoseService } from 'src/app/shared/filter-poses.service';
import { SearchConditionService } from 'src/app/shared/search-conditions.service';
import { UserService } from 'src/app/shared/user.service';
import { VideoService } from 'src/app/shared/video.service';
import { YogaPoseService } from 'src/app/shared/yogapose.service';

@Component({
  selector: 'app-filter-poses',
  templateUrl: './filter-poses.component.html',
  styleUrls: ['./filter-poses.component.css']
})
export class FilterPosesComponent implements OnInit {
  token: string;
  conditions_searched: any;
  contraindicatedPoses: any;
  beneficialPoses: any;
  safePoses: any;
  poseType: string;
  viewType: string;
  shownWorkaround: number;

  constructor(private ConditionsService: ConditionsService,
              private searchConditionService: SearchConditionService,
              private userService: UserService,
              private filterPoseService: FilterPoseService,
              private router: Router,
              private videoService: VideoService,
              private YogaPoseService: YogaPoseService) { }

  ngOnInit() {
    this.searchConditionService.selectedConditions.subscribe(
      (selectedConditions) => {
        this.conditions_searched = selectedConditions;
      });

    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });

    this.filterPoseService.ContraindicatedPoses.subscribe(
      (contraindicatedPoses) => {
        this.contraindicatedPoses = contraindicatedPoses;
      });

    this.filterPoseService.BeneficialPoses.subscribe(
      (beneficialPoses) => {
        this.beneficialPoses = beneficialPoses;
      });

    this.filterPoseService.SafePoses.subscribe(
      (safePoses) => {
        this.safePoses = safePoses;
      });

    this.filterPoseService.poseType.subscribe(
      (poseType) => {
        this.poseType = poseType;
      });

    this.filterPoseService.viewType.subscribe(
      (viewType) => {
        this.viewType = viewType;
      });

    this.filterPoseService.shownWorkaround.subscribe(
      (shownWorkaround) => {
        this.shownWorkaround = shownWorkaround;
      }
    )

    // populate pose categories
    this.filterPoseService.getContraindicatedPoses(this.token, this.conditions_searched);
    this.filterPoseService.getBeneficialPoses(this.token, this.conditions_searched);
    this.filterPoseService.getSafePoses(this.token, this.conditions_searched);
  }

  setPoseType(poseType: string) {
    this.filterPoseService.poseType.next(poseType);
  }

  setViewType(viewType: string) {
    this.filterPoseService.viewType.next(viewType);
  }

  backToSearch() {
    this.router.navigate(['dashboard', 'search-by-condition']);
  }

  viewCondition(condition_id: number) {
    this.ConditionsService.selectCondition(this.token, condition_id);
    this.router.navigate(['dashboard', 'view-condition']);
  }

  viewPose(pose_id: number) {
    this.YogaPoseService.selectPose(this.token, pose_id);
    this.YogaPoseService.getConditionsContraindicatedByPose(pose_id, this.token);
    this.YogaPoseService.getConditionsHelpedByPose(pose_id, this.token);
    this.router.navigate(['dashboard', 'pose-view']);
  }

  viewVideo(pose_video: string) {
    this.videoService.videoUrl.next(pose_video);
    this.router.navigate(['dashboard', 'view-video']);
  }

  showWorkaround(pose_id: number) {
    this.filterPoseService.shownWorkaround.next(pose_id);
    console.log(this.shownWorkaround);
  }
}
