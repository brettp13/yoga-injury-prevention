import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ConditionsService } from 'src/app/shared/conditions.service';
import { UserService } from 'src/app/shared/user.service';

import { SearchConditionService } from 'src/app/shared/search-conditions.service';

@Component({
  selector: 'app-search-component',
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
  token: string;
  conditions: any;
  searchText: string = '';
  toolTipText: string = '';
  areConditionsSelected: boolean = false;
  selectedConditions: any[] = [];
  numberOfSelectedConditions: number = 0;


  // Dynamic sorting table of conditions
  settings = {
    actions: false,
    columns: {
      name: {
        title: 'condition name',
      },
      description: {
        title: 'condition description'
      }
    }
  };

  constructor(private conditionsService: ConditionsService,
              private userService: UserService,
              private router: Router,
              private cdRef: ChangeDetectorRef,
              private searchConditionService: SearchConditionService) { }

  ngOnInit() {
    this.userService.token.subscribe(token => {
      this.token = token;
    });

    this.conditionsService.listOfConditions.subscribe(newListOfConditions => {
      this.conditions = newListOfConditions;
    });

    this.conditionsService.getConditions(this.token);
  }

  selectCondition(condition) {
    this.toolTipText = 'Click to search';
    this.numberOfSelectedConditions += 1;
    this.areConditionsSelected = true;

    if (this.selectedConditions.length > 0) {
      for (var i=0, len=this.selectedConditions.length; i<len; i++) {
        if (condition.id === this.selectedConditions[i].id) {
          this.selectedConditions.push(condition);
        }
      }
    }
  }

  removeCondition(condition: any) {
      console.log('Called `removeCondition`');
      console.log(condition);
  }

  clearConditions() {
      this.selectedConditions = [];
      this.areConditionsSelected = false;
  }

  viewCondition(id: number) {
    this.conditionsService.selectCondition(this.token, id);
    this.conditionsService.searchByConditionBeneficial(this.token, [id]);
    this.conditionsService.searchByConditionSafe(this.token, [id]);
    this.conditionsService.searchByConditionContraindicated(this.token, [id]);
    this.router.navigate(['dashboard', 'view-condition']);
  }
}
