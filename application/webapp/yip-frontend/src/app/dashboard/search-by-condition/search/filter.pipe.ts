import { Pipe, PipeTransform } from '@angular/core';

import { ConditionsService } from '../../../shared/conditions.service'; 

@Pipe({ name: 'conditionFilter' })
export class ConditionFilterPipe implements PipeTransform {
    /**
     * Transform
     * 
     * @param {any[]} items
     * @param {string} searchText
     * @returns {any[]}
     */

     constructor(private conditionsService: ConditionsService) { }

    transform(items: any[], searchText: string): any[] {
        if (!items) {
            return [];
        }
        if (!searchText) {
            return items;
        }

        var results = items.filter(o =>
            Object.keys(o).some(k =>
              String(o[k]).toLowerCase().includes(String(searchText).toLowerCase())));

        this.conditionsService.setSearchResults(results.length);
        return results;
    }
}