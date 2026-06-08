import { Component, OnInit } from '@angular/core';

import { ConditionsService } from '../../shared/conditions.service';
import { UserService } from '../../shared/user.service';
import { UtilsService } from './search/utils.service';

@Component({
  selector: 'app-search-by-condition',
  templateUrl: './search-by-condition.component.html',
  styleUrls: ['./search-by-condition.component.css']
})
export class SearchByConditionComponent implements OnInit {
  token: string;
  conditions: any;

  constructor(private conditionsService: ConditionsService,
              private userService: UserService,
              private utilsService: UtilsService) { }

  ngOnInit() {
    this.userService.token.subscribe(
      (token) => {
        this.token = token;
      });

    this.conditionsService.listOfConditions.subscribe(
      (newListOfConditions) => {
        this.conditions = newListOfConditions;
      });
    
    this.conditionsService.getConditions(this.token);
  }

}
