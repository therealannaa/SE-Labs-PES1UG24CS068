# PSREA UML Component Diagram
You can copy this Mermaid diagram code and paste it into [draw.io](https://app.diagrams.net/) (Arrange > Insert > Advanced > Mermaid) or the [Mermaid Live Editor](https://mermaid.live/) to export your final diagram as PNG or PDF.

```mermaid
%%{init: {'theme': 'base', 'themeVariables': { 'fontFamily': 'arial', 'primaryColor': '#ffffff', 'primaryBorderColor': '#333333', 'lineColor': '#333333'}}}%%
architecture-beta

    %% Define the 5 components
    service ui(server)[User Interface Component]
    service analyzer(server)[Subscription Analyzer Component]
    service importer(server)[Transaction Importer Component]
    service db(database)[Database Component]
    service notify(server)[Notification Service Component]

    %% Define the 4 required interfaces/interactions
    junction analyzer_db
    junction analyzer_importer
    junction analyzer_ui
    junction analyzer_notify

    %% Connect and label the interfaces
    ui:R -- L:analyzer_ui
    analyzer_ui:R -- L:analyzer
    
    analyzer:T -- B:analyzer_importer
    analyzer_importer:T -- B:importer
    
    analyzer:B -- T:analyzer_db
    analyzer_db:B -- T:db
    
    analyzer:R -- L:analyzer_notify
    analyzer_notify:R -- L:notify
```

> **Note**: Mermaid's standard syntax doesn't fully support the UML ball-and-socket notation perfectly without manual SVG tweaking. Since draw.io has built-in UML tools, you may want to use those native tools to drag-and-drop the 5 components (rectangles with `<<component>>`) and 4 ball-and-socket connectors directly. 

### Instructions for Draw.io (Preferred for accurate ball-and-socket)
1. Search for "UML" in Draw.io shapes.
2. Drag 5 **Component** rectangles. Name them:
   - User Interface Component
   - Transaction Importer Component
   - Subscription Analyzer Component
   - Notification Service Component
   - Database Component
3. Drag 4 **Provided/Required Interface** (ball and socket) connection lines:
   - Connect **User Interface** (socket) to **Subscription Analyzer** (ball). Label: `Display Subscription Burn Rate`
   - Connect **Subscription Analyzer** (socket) to **Transaction Importer** (ball). Label: `Request/Receive Data`
   - Connect **Subscription Analyzer** (socket) to **Notification Service** (ball). Label: `Trigger Renewal Alert`
   - Connect **Subscription Analyzer** (socket) to **Database** (ball). Label: `Persist Configs/Data`
