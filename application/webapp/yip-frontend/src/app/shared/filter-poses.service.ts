import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpService } from '../shared/http.service';

import { BehaviorSubject } from 'rxjs';

import { environment } from '../../environments/environment';

@Injectable()
export class FilterPoseService {
    poseType: BehaviorSubject<string> = new BehaviorSubject('Contraindicated');
    viewType: BehaviorSubject<string> = new BehaviorSubject('gallery');
    ContraindicatedPoses: BehaviorSubject<any> = new BehaviorSubject([]);
    BeneficialPoses: BehaviorSubject<any> = new BehaviorSubject([]);
    SafePoses: BehaviorSubject<any> = new BehaviorSubject([]);
    shownWorkaround: BehaviorSubject<any> = new BehaviorSubject(0);

    httpHeaders = {};
    private api_url = environment.API_URL;

    constructor(private http: HttpClient, private httpService: HttpService) { }

    getContraindicatedPoses(token: string, conditions: any[]) {
        var condition_ids: any[] = conditions.map(s=>s.id);
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'conditions': condition_ids};

        this.http.post(
            this.api_url + '/search-by-conditions/get-contraindicated-poses/',
            payload,
            this.httpHeaders
        ).subscribe(
            (response) => {
                console.log(response);
                this.ContraindicatedPoses.next(response);
            },
            (error) => {
                console.log(error);
            }
        )
    }

    getBeneficialPoses(token: string, conditions: any[]) {
        var condition_ids: any[] = conditions.map(s=>s.id);
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'conditions': condition_ids};

        this.http.post(
            this.api_url + '/search-by-conditions/get-beneficial-poses/',
            payload,
            this.httpHeaders
        ).subscribe(
            (response) => {
                console.log(response);
                this.BeneficialPoses.next(response);
            },
            (error) => {
                console.log(error);
            }
        )
    }

    getSafePoses(token: string, conditions: any[]) {
        var condition_ids: any[] = conditions.map(s=>s.id);
        this.httpHeaders = this.httpService.createHeadersWithToken(token);
        var payload = {'conditions': condition_ids};

        this.http.post(
            this.api_url + '/search-by-conditions/get-safe-poses/',
            payload,
            this.httpHeaders
        ).subscribe(
            (response) => {
                console.log(response);
                this.SafePoses.next(response);
            },
            (error) => {
                console.log(error);
            }
        )
    }
}