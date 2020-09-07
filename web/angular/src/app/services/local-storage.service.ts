/**
*HEADER
*           arg/web/angular/src/app/services/local-storage.service.ts
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
import { Inject, Injectable } from '@angular/core';
import { SESSION_STORAGE, StorageService, StorageTranscoders } from 'ngx-webstorage-service';

@Injectable({
  providedIn: 'root'
})
export class LocalStorageService {

  private numberStorage: StorageService<number>;
  private jsonStorage: StorageService<any>;
  private stringStorage: StorageService<string>;
  private booleanStorage: StorageService<boolean>;

  public static CONF_KEY: string = 'configuration';
  public static IS_DEFAULT_CONF: string = 'is_default_configuration';

  public static ARG_PARAMETERS_KEY: string = 'parameters';
  public static ARG_RUN_OPT_KEY: string = 'run_opt';

  /**
   * @constructor
   * @param @Inject(SESSION_STORAGE [description]
   */
  constructor(@Inject(SESSION_STORAGE) private storage: StorageService) {
      this.numberStorage = this.storage.withDefaultTranscoder(StorageTranscoders.NUMBER);
      this.jsonStorage = this.storage.withDefaultTranscoder(StorageTranscoders.JSON);
      this.stringStorage = this.storage.withDefaultTranscoder(StorageTranscoders.STRING);
      this.booleanStorage = this.storage.withDefaultTranscoder(StorageTranscoders.BOOLEAN);

      if (!this.jsonStorage.has(LocalStorageService.ARG_PARAMETERS_KEY))
        this.jsonStorage.set(LocalStorageService.ARG_PARAMETERS_KEY, {})  
  }

  /**
   * Set item json
   */
  public setJson(key: string, value: any) {
    return this.jsonStorage.set(key, value);
  }

  /**
   * Get item json
   */
  public getJson(key: string): any {
    return this.jsonStorage.get(key);
  }

  /**
   * Set item boolean
   */
  public setBoolean(key: string, value: boolean) {
    return this.booleanStorage.set(key, value);
  }

  /**
   * Get item boolean
   */
  public getBoolean(key: string): boolean {
    return this.booleanStorage.get(key);
  }

  /**
   * Set item number
   */
  public setNumber(key: string, value: number) {
    return this.numberStorage.set(key, value);
  }

  /**
   * Get item number
   */
  public getNumber(key: string): number {
    return this.numberStorage.get(key);
  }

  /**
   * Set item string
   */
  public setString(key: string, value: string) {
    return this.stringStorage.set(key, value);
  }

  /**
   * Get item string
   */
  public getString(key: string): string {
    return this.stringStorage.get(key);
  }
}
