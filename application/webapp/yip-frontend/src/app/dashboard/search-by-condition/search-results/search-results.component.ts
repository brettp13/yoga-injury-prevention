import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ConditionsService } from '../../../shared/conditions.service';
import { UserService } from '../../../shared/user.service';
import { YogaPoseService } from '../../../shared/yogapose.service';

@Component({
  selector: 'app-search-results',
  templateUrl: './search-results.component.html',
  styleUrls: ['./search-results.component.css']
})
export class SearchResultsComponent implements OnInit {
  token: string;
  searchResults: any;

  constructor(private conditionsService: ConditionsService,
              private userService: UserService,
              private yogaPoseService: YogaPoseService,
              private router: Router) { }

  ngOnInit() {
    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });
    
    this.conditionsService.beneficialConditionSearchResults.subscribe(
      (searchResults) => {
        this.searchResults = searchResults;
      });

    this.conditionsService.safeConditionSearchResults.subscribe(
      (searchResults) => {
        this.searchResults = searchResults;
      });

    this.conditionsService.contraindicatedConditionSearchResults.subscribe(
      (searchResults) => {
        this.searchResults = searchResults;
      });
  }

  returnToSearchByPose() {
    this.router.navigate(['dashboard', 'search-by-condition']);
  }

  viewPose(id: number) {
    this.yogaPoseService.selectPose(this.token, id);
    this.yogaPoseService.getConditionsContraindicatedByPose(id, this.token);
    this.yogaPoseService.getConditionsHelpedByPose(id, this.token);
    this.yogaPoseService.cameFrom.next('conditions');
    this.router.navigate(['dashboard', 'pose-view'])
  }

  viewCondition(id: number) {
    this.conditionsService.selectCondition(this.token, id);
    this.conditionsService.searchByConditionBeneficial(this.token, [id]);
    this.conditionsService.searchByConditionSafe(this.token, [id]);
    this.conditionsService.searchByConditionContraindicated(this.token, [id]);
    this.router.navigate(['dashboard', 'view-condition']);
  }
}
