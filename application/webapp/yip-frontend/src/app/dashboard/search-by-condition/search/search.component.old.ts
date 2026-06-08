import { Component, OnInit } from '@angular/core';
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
  toolTipText: string = 'Select at least (1) condition below';
  areConditionsSelected: boolean = false;
  selectedConditions: any[] = [];
  numberOfSelectedConditions: number = 0;
  searchResults: number;

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
              private searchConditionService: SearchConditionService) { }

  ngOnInit() {
    this.userService.token.subscribe(token => {
      this.token = token;
    });

    this.conditionsService.listOfConditions.subscribe(newListOfConditions => {
      this.conditions = newListOfConditions;
    });

    this.conditionsService.getConditions(this.token);

    this.conditionsService.setSearchResults(0);

    this.conditionsService.searchResults.subscribe(
      (results) => {
        this.searchResults = results;
      });

    this.searchConditionService.selectedConditions.subscribe(
      (selectedConditions) => {
        this.selectedConditions = selectedConditions;
      });
  }

  selectCondition(condition) {
    var push: boolean = true;
    this.areConditionsSelected = true;
    this.toolTipText = 'Click to search';
    this.numberOfSelectedConditions += 1;
    if (this.selectedConditions.length > 0) {
      for (var i=0, len=this.selectedConditions.length; i<len; i++) {
        if (condition.id === this.selectedConditions[i].id) {
          push = false;
        }
      }
    }
    if (push) {
      //this.selectedConditions.push(condition);
      //console.log(this.selectedConditions);
      this.searchConditionService.addConditionToSelected(condition);
    }
  }

  removeCondition(condition: any) {
    //this.numberOfSelectedConditions -= 1;
    this.searchConditionService.removeConditionFromSelected(condition)
    
    
    //for (var i=0, len=this.selectedConditions.length; i<len; i++) {
      //if (id === this.selectedConditions[i].id) {
        //this.selectedConditions.splice(i, 1);
        //if (this.selectedConditions.length === 0) {
          //this.areConditionsSelected = false;
          //this.toolTipText = 'Select at least (1) condition below';
        //}
      //}
    //}
  }
  
  clearConditions() {
    this.searchConditionService.clearConditions();
  }

  returnBeneficialPoses() {
    // grab the ids of the selected conditions
    var selectedConditionIds = [];
    for (var condition of this.selectedConditions) {
      selectedConditionIds.push(condition.id);
    }
    this.conditionsService.searchByConditionBeneficial(this.token, selectedConditionIds);
    this.router.navigate(['dashboard', 'search-by-condition', 'search-results']);
  }

  returnSafePoses() {
    // grab the ids of the selected conditions
    var selectedConditionIds = [];
    for (var condition of this.selectedConditions) {
      selectedConditionIds.push(condition.id);
    }
    this.conditionsService.searchByConditionSafe(this.token, selectedConditionIds);
    this.router.navigate(['dashboard', 'search-by-condition', 'search-results']);
  }

  returnUnsafePoses() {
    // grab the ids of the selected conditions
    var selectedConditionIds = [];
    for (var condition of this.selectedConditions) {
      selectedConditionIds.push(condition.id);
    }
    this.conditionsService.searchByConditionContraindicated(this.token, selectedConditionIds);
    this.router.navigate(['dashboard', 'search-by-condition', 'search-results']);
  }

  clearSelectedConditions() {
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
