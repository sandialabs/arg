/**
*HEADER
*           arg/web/angular/src/app/tabs/inserts/inserts.component.ts
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

// Services
import { EventService } from './../../services/event.service';
import { LocalStorageService } from './../../services/local-storage.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-inserts',
  templateUrl: './inserts.component.html',
  styleUrls: ['./inserts.component.scss']
})
export class InsertsComponent implements OnInit {
  /**
   * @variables
   */
   public INSERTTYPES = [
      "string",
      "image"
   ]

  private defaultFormValues = {
    Insert: [],
  }
  public form = new FormGroup({
    Insert: new FormControl(this.defaultFormValues.Insert)
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
    this.eventService.subscribe('inserts-tab-refresh',
      (data: any) => {
        if ("object" == typeof data) {
          this.form.reset();
          let formData: any = this.defaultFormValues;

          // If insert key not present empty Insert array
          if (data['Insert'] === undefined)
            formData['Insert'] = [];

          // Prepare new data
          Object.keys(data).forEach((key) => {
            if (this.form.contains(key)) {
              if (typeof data[key] == 'number') {
                data[key] = data[key].toString();
              }
              formData[key] = data[key];
            }
          });
          // Set form data
          this.form.setValue(formData);
        }
      }
    );

    // Refresh the first time
    this.eventService.publish('inserts-tab-refresh', this.localStorageService.getJson(LocalStorageService.ARG_PARAMETERS_KEY));

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

  updateLocation(index: 'number', insert: object, event: any): void {
    let formData: any = this.form.value;
    const newLocation = event.target.textContent;
    if (newLocation != ""  && (newLocation != insert["location"] )) {
      formData["Insert"][index].location = newLocation;
    }

    // Set form data
    this.form.setValue(formData);
  }

  updateTextOrImage(index: 'number', insert: object, event: any): void {
    let formData: any = this.form.value;
    const newText = event.target.textContent;
    console.log("newText: "+newText +" " + event)
    var type = insert["string"] ? this.INSERTTYPES[0] : this.INSERTTYPES[1];
    if (newText != ""  && (newText != insert[type] )) {
       formData["Insert"][index][type]= [newText];
    }

    // Set form data
    event.target.textContent = newText;
    this.form.setValue(formData);
   }

  updateTypes(index: 'number', insert: object, event: any): void {
    let formData: any = this.form.value;
    const newType = event.target.value;
    var oldType = insert["string"] ? this.INSERTTYPES[0] : this.INSERTTYPES[1];

    if (newType != ""  && (newType != oldType )) {
      formData["Insert"][index][newType] = formData["Insert"][index][oldType];
      delete formData["Insert"][index][oldType];
      var test=0;
    }
    // Set form data
    this.form.setValue(formData);
   }

   addInsert(): void {
     let formData: any = this.form.value;
     var nextNumberNameRequested = formData["Insert"].length;
     formData["Insert"][nextNumberNameRequested] = {};
     formData["Insert"][nextNumberNameRequested].location = "1";
     formData["Insert"][nextNumberNameRequested][this.INSERTTYPES[0]] = ["My insertion"];
     // Set form data
     this.form.setValue(formData);
   }

   removeInsert(index: 'number'): void {
     let formData: any = this.form.value;
     var nextNumberNameRequested = formData["Insert"].length;
     formData["Insert"].splice(index, 1);
     // Set form data
     this.form.setValue(formData);
   }

  getInsertType(insert: object): string {
    var result =  insert[this.INSERTTYPES[0]] ? this.INSERTTYPES[0] : this.INSERTTYPES[1];
    return result;
  }
}
