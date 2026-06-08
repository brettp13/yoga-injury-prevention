import { Injectable } from '@angular/core';

@Injectable()
export class UtilsService {
    // Helper functions

    compareArrays(array1: any[], array2: any[]) {
        console.log(array1);
        console.log(array2);
        if (array1.length === 0 && array2.length === 0) {
            console.log('both arrays are empty');
            return true;
        }
        else if (array1.length !== array2.length) {
            console.log('length of arrays does not match');
            console.log(array1.length);
            console.log(array2.length);
            return false;
        }
        else if (array1.length === array2.length) {
            console.log('length of arrays match');
            for (var i=0, len=array1.length; i<len; i++) {
                if (array1[i] !== array2[i]) {
                    console.log('length of arrays matches, but objects inside of arrays do not');
                    return false;
                }
            }
            return true;
        }
        else {
            console.log('None of the above turned out to be true');
            return true;
        }
    }
}