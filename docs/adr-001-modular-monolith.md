# ADR-001: Start the hotel booking app as a modular monolith

Status: Accepted, 30 October 2026

## Context
One small team builds and releases the application. Rooms, Reservations, Payments and Notifications have distinct responsibilities. S2 (no double booking) and S3 (notification failure keeps booking) matter most. There is no measured need for independent releases or scaling.

## Decision
Use one console application with four modules, public contracts, private implementation folders and executable architecture checks. Reservations owns the booking rule. Program.cs wires concrete implementations. Other modules use public contracts only.

## Alternatives considered
A single unstructured application mixes responsibilities and makes provider changes risky. Separate services permit independent deployment but introduce partial failures, retries, multiple deployments and monitoring without a current requirement for them.

## Consequences
One build and deployment, local calls and isolated adapters simplify development. All modules still release together; namespace boundaries require tests. S3 is covered by a failure test. S2 is not solved by module separation: the P03 race intentionally remains until P09. Payments is simulated; no charge is performed by Reserve.

## Revisit when
Measured load, an independent release schedule or separate team ownership justifies extracting a module. Do not split on speculation.
