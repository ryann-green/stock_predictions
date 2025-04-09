# Stock Prediction Process Flow

## Overview
This document outlines the flow of the stock prediction process in the app. The flow includes interactions between the **Client**, **Server**, and **Service** components, with a clear loop for iterative predictions.

---

### **Flowchart**
```mermaid
sequenceDiagram
Client ->> Server: Request Stock Predictions
activate Server
Server ->> Service: Fetch Missing Dates

loop until success
  Service ->> Service: Load Historical Data
  Service ->> Service: Generate Features
  Service ->> Service: Train & Evaluate Models
  Service ->> Service: Compute Success Rates
end

Service ->> Server: Aggregate Prediction Results
Server --> Client: Return Results
deactivate Server
