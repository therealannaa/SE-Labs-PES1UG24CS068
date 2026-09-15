# Architectural Justification: PSREA Project

## Architecture Selection
For the **Personal Subscription & Recurring Expense Analyzer (PSREA)**, an advanced **Layered Architecture** was selected. The system is structurally divided into three distinct vertical tiers: 
1. **Presentation Layer**: Hosting the `Client Application` subsystem (including the Dashboard View, Alerts Configurator, and Session Auth).
2. **Business Layer**: Hosting the core processing subsystems (`Core Analysis Engine`, `Banking Integration`, and `Notification Service`).
3. **Data Layer**: Hosting the `Data Storage` subsystem (Transaction DB and User Profiles DB).

## Specific Scenario-Related Reasons
1. **Hierarchical Separation of Concerns**: PSREA relies heavily on a mixture of external API streams (banking integrations), complex analytics, and dynamic UI dashboards. The layered architecture tightly groups related internal modules (like grouping the *Bank Access Client* and *API Gateway* strictly inside the Banking subsystem) while enforcing strict boundary interfaces. Based on this design, the UI never connects to the Bank API directly; it exclusively interacts with the Analysis Engine.
2. **System Scalability and Maintainability**: By isolating the computationally heavy `Core Analysis Engine` (responsible for the *Recurring Detector* and *Data Normalizer*) into the Business Layer, the system can scale its background processing independently of the presentation layer. If a new third-party banking integration is adopted, only the `Banking Integration` subsystem requires an update, entirely insulating the frontend UI and the detection algorithms from breaking changes.

## Security Advantage
The Layered Architecture inherently addresses critical financial data security concerns through isolated encapsulation. The `Secure Transaction DB`, which stores highly sensitive banking transaction histories, sits safely at the bottom Data Layer and is completely partitioned off from the Presentation Layer. Direct database access is structurally impossible for front-end clients; it can uniquely only be accessed through the tightly controlled `Read/Write Tx` interface provided to the `Core Analysis Engine`. This ensures that raw bank data is centralized securely inside the trusted business tier, preventing malicious direct querying.

## Performance Benefit
PSREA features a strict performance constraint requiring dashboard rendering and analysis workflows to be highly responsive, ideally displaying data well under 60-second turnarounds. The Layered Architecture allows the `Monthly Aggregator` component—located centrally within the `Core Analysis Engine`—to run asynchronously in the background layer and cache evaluated subscription metrics. When the `Dashboard View` in the Presentation Layer requests data via the `Analytics API`, the backend simply serves the pre-calculated metrics rather than executing an expensive real-time re-scan of the entire database, guaranteeing low-latency UX rendering and satisfying performance thresholds.
