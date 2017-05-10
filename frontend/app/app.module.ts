import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpModule } from '@angular/http';
import { MaterialModule } from '@angular/material';

import { AppComponent } from './app.component';


@NgModule({
    declarations: [
        AppComponent,
    ], 
    imports: [
        BrowserModule,
        MaterialModule.forRoot(),
        // BrowserAnimationsModule,
        HttpModule,
        // AppRoutingModule
    ], 
    bootstrap: [AppComponent]
})
export class AppModule {
    name: string = "";
}
