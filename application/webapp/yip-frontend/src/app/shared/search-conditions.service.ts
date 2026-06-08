import { Injectable } from '@angular/core';

import { BehaviorSubject } from 'rxjs';

@Injectable()
export class SearchConditionService {
    selectedConditions: BehaviorSubject<any[]> = new BehaviorSubject([]);

    constructor() { }
}