import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { ConditionsService } from 'src/app/shared/conditions.service';
import { SearchConditionService } from 'src/app/shared/search-conditions.service';
import { UserService } from 'src/app/shared/user.service';

@Component({
    selector: 'app-search-component',
    templateUrl: './search.component.html',
    styleUrls: ['./search.component.css']
})
export class SearchComponent implements OnInit {
    token: string;
    conditions: any;
    searchText: string = '';
    toolTipText: string = 'Select at least (1) condition below to search';
    areConditionsSelected: boolean;
    selectedConditions: any[] = [];
    numberOfSelectedConditions: number;

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

    constructor(private conditionService: ConditionsService,
                private router: Router,
                private userService: UserService,
                private searchConditionService: SearchConditionService) { };

    ngOnInit() {
        this.userService.token.subscribe(
            (token) => {
                this.token = token;
            });

        this.conditionService.listOfConditions.subscribe(
            (conditions) => {
                this.conditions = conditions;
            });

        this.searchConditionService.selectedConditions.subscribe(
            (listOfSelectedConditions) => {
                this.selectedConditions = listOfSelectedConditions;
            });

        this.conditionService.getConditions(this.token);

        this.conditionService.numberOfSelectedConditions.subscribe(
            (numberOfSelectedConditions) => {
                this.numberOfSelectedConditions = numberOfSelectedConditions;
            });

        this.conditionService.areConditionsSelected.subscribe(
            (areConditionsSelected) => {
                this.areConditionsSelected = areConditionsSelected;
            });

    };

    selectCondition(condition) {
        var push: boolean = true;

        if (this.selectedConditions.length > 0) {
            // if we already have some selected conditions, make sure we're not double selecting
            for (var i=0, len=this.selectedConditions.length; i<len; i++) {
                if (condition.id === this.selectedConditions[i].id) {
                    this.removeCondition(condition);
                    push = false
                }
            }
        }
        if(push) {
            this.conditionService.numberOfSelectedConditions.next(
                this.numberOfSelectedConditions += 1);
            this.conditionService.areConditionsSelected.next(
                this.areConditionsSelected = true);
            this.selectedConditions.push(condition);
            this.searchConditionService.selectedConditions.next(this.selectedConditions);
        }
    }

    removeCondition(condition) {
        this.conditionService.numberOfSelectedConditions.next(
            this.numberOfSelectedConditions -= 1);

        for (var i=0, len=this.selectedConditions.length; i<len; i++) {
    
            if (condition.id === this.selectedConditions[i].id) {
                this.selectedConditions.splice(i, 1);
                this.searchConditionService.selectedConditions.next(
                    this.selectedConditions);
        
                if (this.selectedConditions.length === 0) {
                    this.conditionService.areConditionsSelected.next(
                        this.areConditionsSelected = false);
                    this.toolTipText = 'Select at least (1) condition below';
                }
            }
        }
    }

    clearConditions() {
        this.searchConditionService.selectedConditions.next([]);
        this.numberOfSelectedConditions = 0;
        this.areConditionsSelected = false;
    }

    viewPoses() {
        this.router.navigate(['dashboard', 'search-by-condition', 'filter-poses'])
    }

}