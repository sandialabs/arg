/**
*HEADER
*      arg/web/angular/src/app/tabs/data-options/data-options.component.ts
*                Automatic Report Generator (ARG) v. 1.0
*
*  Copyright 2020 National Technology & Engineering Solutions of Sandia, LLC
*  (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
*  Government retains certain rights in this software.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions are met:
*
*  * Redistributions of source code must retain the above copyright notice,
*    this list of conditions and the following disclaimer.
*
*  * Redistributions in binary form must reproduce the above copyright notice,
*    this list of conditions and the following disclaimer in the documentation
*    and/or other materials provided with the distribution.
*
*  * Neither the name of the copyright holder nor the names of its
*    contributors may be used to endorse or promote products derived from this
*    software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
*  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
*  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
*  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
*  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
*  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUENT OF
*  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
*  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
*  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
*  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
*  POSSIBILITY OF SUCH DAMAGE.
*
*  Questions? Visit gitlab.com/AutomaticReportGenerator/arg
*
*HEADER
*/
// Libs
import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { Subscription } from 'rxjs';

// Services
import { EventService } from './../../services/event.service';
import { LocalStorageService } from './../../services/local-storage.service';


@Component({
  selector: 'app-data-options',
  templateUrl: './data-options.component.html',
  styleUrls: ['./data-options.component.scss']
})

export class DataOptionsComponent implements OnInit {
  /**
   * @variables
   */

  public TABLESMAPPING = {
      CADToFEM: "CADToFEM",
      FEMToCAD: "FEMToCAD"
  }

  private defaultFormValues = {
    DataDirectory: '',
    GeometryRoot: '',
    ReportedCadMetaData: '',
    DeckRoot: '',
    IgnoredBlockKeys: '',
    Mappings: {
        FEM_to_CAD: {
            elements: {},
            factors: {}
        },
        CAD_to_FEM: {
            elements: {},
            factors: {}
        }
    },
    CADtoFEM: [{}],
    FEMtoCAD: [{}]
  }
  public form = new FormGroup({
    DataDirectory: new FormControl(this.defaultFormValues.DataDirectory),
    GeometryRoot: new FormControl(this.defaultFormValues.GeometryRoot),
    ReportedCadMetaData: new FormControl(this.defaultFormValues.ReportedCadMetaData),
    DeckRoot: new FormControl(this.defaultFormValues.DeckRoot),
    IgnoredBlockKeys: new FormControl(this.defaultFormValues.IgnoredBlockKeys),
    Mappings: new FormControl(Object.assign({}, this.defaultFormValues.Mappings)),
    CADtoFEM: new FormControl(this.defaultFormValues.CADtoFEM),
    FEMtoCAD: new FormControl(this.defaultFormValues.FEMtoCAD)
  });
  valueChangesSubscription: Subscription;

  /**
   * @constructor
   */
  constructor(
    private eventService: EventService,
    private localStorageService: LocalStorageService
  ) { }

  /**
   * OnInit
   *
   * @return {void}
   */
  ngOnInit(): void {
    // Refresh listener
    this.eventService.subscribe('data-options-tab-refresh',
      (data: any) => {
        if ("object" == typeof data) {
          // Reset form
          this.form.reset();

          // Get defaults
          let formData: any = this.defaultFormValues;

          // Prepare new data
          Object.keys(data).forEach((key) => {
            
            if (this.form.contains(key)) {
              if (typeof data[key] == 'number') {
                data[key] = data[key].toString();
              }
              if (typeof data[key] == 'object') {
                if (key != 'Mappings') {
                    data[key] = data[key].join(';');
                }
              }
              
              if (formData[key] !== data[key]){
                if (key == 'Mappings') {
                  formData[key].FEM_to_CAD = Object.assign(
                    { elements: {}, factors: {}}, 
                    data[key].FEM_to_CAD ? data[key].FEM_to_CAD : {}
                  );
                  formData[key].CAD_to_FEM = Object.assign(
                    { elements: {}, factors: {}}, 
                    data[key].CAD_to_FEM ? data[key].CAD_to_FEM : {}
                  );
                }
                else {
                  formData[key] = data[key];
                }
              }
            }

          });

          // Set form data
          this.form.setValue(formData);
        }
      }
    );

    // Refresh the first time
    this.eventService.publish('data-options-tab-refresh', this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY));

    // form value change listener
    this.valueChangesSubscription = this.form.valueChanges.subscribe(val => {
      // Get current storage configuration
      var currentConfig = this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY);
      var state = JSON.stringify(currentConfig);
      var configUpdate = Object.assign(currentConfig, val);
      if (state != JSON.stringify(configUpdate)){
        this.localStorageService.setJson(LocalStorageService.ARG_PARAMETERS_KEY, configUpdate);
      }
    });
  }

  /**
   * Returns a new key for an array using a prefix and a number suffix
   * This method will recursively increment the suffix until it finds a non-existing key
   * @param arr The array to identify a new key for.
   * @param prefix a string prefix
   * @param numberSuffix the number suffix to verify
   */
  createUniqueKey(arr: any, prefix: string, numberSuffix: number): string {
     
    if (arr == null){
      console.error("Invalid array : " + arr);
      return null;
    }
    else {

      if (arr.elements[prefix + numberSuffix] !== undefined)
      {
        return this.createUniqueKey(arr, prefix, numberSuffix + 1);
      }
      else return prefix + numberSuffix;
    }
  }

  /**
   * 
   * @param table Adds an element to a table (Mappings.FEM_to_CAD or Mappings.CAD_to_FEM)
   */
  addElt(table: string): void {

    let formData: any = this.form.value;

    let arr = null;
    if (table == this.TABLESMAPPING.CADToFEM ) {
      arr = formData.Mappings.CAD_to_FEM;
    }
    else if (table ==  this.TABLESMAPPING.FEMToCAD ) {
      arr = formData.Mappings.FEM_to_CAD;
    }

    if (arr !== null){
      var nbElements = Object.keys(arr.elements).length;
      var newKey = this.createUniqueKey(arr, "elt", nbElements);
      arr.elements[newKey] =[];
      arr.factors[newKey] ='';

      // Set form data
      this.form.setValue(formData);
    }
    else console.error("addElt : Invalid table id " + table);
  }

  removeElementsAndFactors(table: any, key: string) {
      delete table.elements[key];
      delete table.factors[key];
  }

  removeElt(table: string, key: string): void {
    let formData: any = this.form.value;
    if (table == this.TABLESMAPPING.CADToFEM ) {
        this.removeElementsAndFactors(formData.Mappings.CAD_to_FEM, key);
    }
    else if (table ==  this.TABLESMAPPING.FEMToCAD ) {
        this.removeElementsAndFactors(formData.Mappings.FEM_to_CAD, key);
    }
    this.form.setValue(formData);
  }

   updateCol1ElementsAndFactors(table: any, newKey: string, oldKey: string) {
       table.elements[newKey] = table.elements[oldKey];
       table.factors[newKey] = table.factors[oldKey];
       delete table.elements[oldKey];
       delete table.factors[oldKey];
   }
   updateCol1(table: string, oldKey: string, event: any) {
       let formData: any = this.form.value;
       const newKey = event.target.textContent;
       if (oldKey != newKey) {
           if (table == this.TABLESMAPPING.CADToFEM ) {
               this.updateCol1ElementsAndFactors(formData.Mappings.CAD_to_FEM, newKey, oldKey);
           }
           else if (table ==  this.TABLESMAPPING.FEMToCAD ) {
               this.updateCol1ElementsAndFactors(formData.Mappings.FEM_to_CAD, newKey, oldKey);
           }
           this.form.setValue(formData);
       }
   }

  updateCol2(table: string, key: string, event: any) {
      let formData: any = this.form.value;
      const col2 = event.target.textContent;
      if (table == this.TABLESMAPPING.CADToFEM ) {
          formData.Mappings.CAD_to_FEM.elements[key] = col2.split(';');
      }
      else if (table ==  this.TABLESMAPPING.FEMToCAD ) {
          formData.Mappings.FEM_to_CAD.elements[key] = col2.split(';');
      }
      this.form.setValue(formData);
  }

  updateCol3(table: string, key: string, event: any) {
      let formData: any = this.form.value;
      const newFactor = event.target.textContent;
      if (table == this.TABLESMAPPING.CADToFEM ) {
          formData.Mappings.CAD_to_FEM.factors[key] = newFactor
      }
      else if (table ==  this.TABLESMAPPING.FEMToCAD ) {
          formData.Mappings.FEM_to_CAD.factors[key] = newFactor
      }
      this.form.setValue(formData);
   }

  ngOnDestroy() {
      this.valueChangesSubscription.unsubscribe()
  }
}
