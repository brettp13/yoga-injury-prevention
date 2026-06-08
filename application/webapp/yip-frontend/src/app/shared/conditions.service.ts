import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';

import { BehaviorSubject } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable()
export class ConditionsService {
    httpHeaders = {};
    private api_url = environment.API_URL;

    beneficialConditionSearchResults: BehaviorSubject<any>;
    safeConditionSearchResults: BehaviorSubject<any>;
    contraindicatedConditionSearchResults: BehaviorSubject<any>;
    listOfConditions: BehaviorSubject<any>;
    selectedCondition: BehaviorSubject<any>;
    howYogaHelps: BehaviorSubject<any>;
    searchResults: BehaviorSubject<number>;
    numberOfSelectedConditions: BehaviorSubject<number>;
    areConditionsSelected: BehaviorSubject<boolean>;

    constructor (private http: HttpClient, private httpService: HttpService) {
        this.safeConditionSearchResults = new BehaviorSubject([]);
        this.beneficialConditionSearchResults = new BehaviorSubject([]);
        this.contraindicatedConditionSearchResults = new BehaviorSubject([]);
        this.listOfConditions = new BehaviorSubject([]);
        this.selectedCondition = new BehaviorSubject([]);
        this.howYogaHelps = new BehaviorSubject([]);
        this.searchResults = new BehaviorSubject(0);
        this.numberOfSelectedConditions = new BehaviorSubject(0);
        this.areConditionsSelected = new BehaviorSubject(false);
    };

    newBeneficialConditionSearchResults(searchResults: any) {
        console.log('Beneficial Poses For Search');
        console.log(searchResults);
        this.beneficialConditionSearchResults.next(searchResults);
    }

    newSafeConditionSearchResults(searchResults: any) {
        console.log('Safe Poses For Search');
        console.log(searchResults);
        this.safeConditionSearchResults.next(searchResults);
    }

    newContraindicatedSearchResults(searchResults: any) {
        console.log('Contraindicated Poses For Search');
        console.log(searchResults);
        this.contraindicatedConditionSearchResults.next(searchResults);
    }

    newListOfConditions(conditions: any) {
        this.listOfConditions.next(conditions);
    }
    
    getConditions(token: string) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        this.http.get(this.api_url + '/conditions/list-conditions/', this.httpHeaders)
          .subscribe(
              (response) => {
                  this.newListOfConditions(response);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    selectCondition(token:string, id: number) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'condition_id': id};
        this.http.post(
            this.api_url + '/conditions/select-condition/',
            payload,
            this.httpHeaders
        ).subscribe(
            (response) => {
                this.selectedCondition.next(response);
            },
            (error) => {
                console.log(error);
            }
        )
    }

    searchByConditionBeneficial(token: string, conditions: any) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'conditions': conditions};
        this.http.post(
            this.api_url + '/search-by-conditions/get-beneficial-poses/',
            payload, 
            this.httpHeaders
        ).subscribe(
            (response: Response) => {
                this.newBeneficialConditionSearchResults(response);
                console.log(response);
            },
            (error) => {
                console.log(error);
            }
        )
    }

    searchByConditionSafe(token: string, conditions: any) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'conditions': conditions};
        this.http.post(
            this.api_url + '/search-by-conditions/get-safe-poses/',
            payload, 
            this.httpHeaders
        ).subscribe(
            (response) => {
                this.newSafeConditionSearchResults(response);
                console.log(response);
            },
            (error) => {
                console.log(error);
            }
        )
    }

    searchByConditionContraindicated(token: string, conditions: any) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'conditions': conditions};
        this.http.post(
            this.api_url + '/search-by-conditions/get-contraindicated-poses/',
            payload,
            this.httpHeaders
        ).subscribe(
            (response) => {
                this.newContraindicatedSearchResults(response);
                console.log(response);
            },
            (error) => {
                console.log(error);
            }
        )
    }

    getHowYogaHelps(token: string, condition_id: number) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'condition_id': condition_id}
        this.http.post(
            this.api_url + '/search-by-conditions/how-yoga-can-help/',
            payload,
            this.httpHeaders
        ).subscribe(
            (response) => {
                this.howYogaHelps.next(response);
                console.log(response);
            },
            (error) => {
                console.log(error);
            }
        )
    }

    setSearchResults(numberOfResults: number) {
        this.searchResults.next(numberOfResults);
    }

}