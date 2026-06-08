import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';

import { BehaviorSubject } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable()
export class YogaPoseService {
    httpHeaders = {};
    private api_url = environment.API_URL;

    listOfPoses: BehaviorSubject<any>;
    selectedPose: BehaviorSubject<any>;
    conditionsHelped: BehaviorSubject<any>;
    conditionsContraindicated: BehaviorSubject<any>;
    listView: BehaviorSubject<boolean>;
    yogaStyles: BehaviorSubject<any>;

    searchResults: BehaviorSubject<number>;

    // to show where user hit the viewPose page from
    cameFrom: BehaviorSubject<String>;

    constructor (private http: HttpClient,
                 private httpService: HttpService) 
    {
        this.listOfPoses = new BehaviorSubject([]);
        this.conditionsHelped = new BehaviorSubject([]);
        this.conditionsContraindicated = new BehaviorSubject([]);
        this.selectedPose = new BehaviorSubject([]);
        this.listView = new BehaviorSubject(true);
        this.cameFrom = new BehaviorSubject('');
        this.yogaStyles = new BehaviorSubject([]);
        this.searchResults = new BehaviorSubject(0);
    };

    newListOfPoses(poses: any) {
        this.listOfPoses.next(poses);
    }

    newConditionsHelped(conditions: any) {
        this.conditionsHelped.next(conditions);
    }

    newConditionsContraindicated(conditions: any) {
        this.conditionsContraindicated.next(conditions)
    }

    setSearchResults(results: number) {
        this.searchResults.next(results);
    }

    getPoses(token: string) {
        console.log('Trying to get a new list of poses');
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        this.http.get(this.api_url + '/yoga-poses/list-poses/', this.httpHeaders)
          .subscribe(
              (response) => {
                  console.log(response);
                  this.newListOfPoses(response);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    selectPose(token: string, pose_id: number) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'yoga_pose_id': pose_id};
        console.log(payload);
        this.http.post(this.api_url + '/yoga-poses/select-pose/', payload, this.httpHeaders)
          .subscribe(
              (response) => {
                  console.log(response);
                  this.selectedPose.next(response);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    getConditionsHelpedByPose(pose_id: number, token: string) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'yoga_pose_id': pose_id};
        this.http.post(this.api_url + '/search-by-pose/get-conditions-helped-by-pose/', payload, this.httpHeaders)
          .subscribe(
              (response) => {
                  console.log(response);
                  this.newConditionsHelped(response);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    getConditionsContraindicatedByPose(pose_id: number, token: string) {
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'yoga_pose_id': pose_id};
        this.http.post(this.api_url + '/search-by-pose/get-conditions-contraindicated-by-pose/', payload, this.httpHeaders)
          .subscribe(
              (response) => {
                  console.log(response);
                  this.newConditionsContraindicated(response);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    getYogaStyles() {
        this.httpHeaders = this.httpService.createHeadersNoToken();
        this.http.get(this.api_url + '/profile/list-yoga-styles')
          .subscribe(
              (yogaStyles) => {
                  this.yogaStyles.next(yogaStyles);
              },
              (error) => {
                  console.log(error);
              }
          )
    }

    setListView() {
        this.listView.next(!this.listView.value);
    }
}