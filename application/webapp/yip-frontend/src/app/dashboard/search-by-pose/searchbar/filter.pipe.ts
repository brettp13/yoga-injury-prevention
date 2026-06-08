import { Pipe, PipeTransform } from '@angular/core';

import { YogaPoseService } from '../../../shared/yogapose.service';

@Pipe({ name: 'yogaPoseFilter' })
export class FilterPipe implements PipeTransform {
  /**
   * Transform
   *
   * @param {any[]} items
   * @param {string} searchText
   * @returns {any[]}
   */

  constructor(private yogaPoseService: YogaPoseService) { }

  transform(items: any[], searchText: string): any[] {
    if (!items) {
      return [];
    }
    if (!searchText) {
      return items;
    }

    var results = items.filter(o =>
      Object.keys(o).some(k =>
        String(o['english_name']).toLowerCase().includes(String(searchText).toLowerCase()) 
        ||  String(o['sanskrit_name']).toLowerCase().includes(String(searchText).toLowerCase())));
    
    this.yogaPoseService.setSearchResults(results.length);
    return results;
  }
}
