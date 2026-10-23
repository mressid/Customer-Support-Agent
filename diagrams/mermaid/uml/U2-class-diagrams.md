# U2 — UML Class Diagrams

Design-level classes for the modular monolith. Names follow the module catalog (`02-module-catalog.md`) and domain model (`05-domain-model.md`). Attributes and operations are proposals for implementation, not final signatures. One diagram per module group keeps each readable.

## U2.1 Access and tenancy (M18)

```mermaid
classDiagram
    class Organization {
        +UUID id
        +String name
        +Settings settings
        +DateTime createdAt
    }
    class User {
        +UUID id
        +String email
        +String displayName
    }
    class Membership {
        +UUID id
        +MembershipStatus status
        +revoke()
    }
    class Role {
        +UUID id
        +String name
        +hasPermission(p) bool
    }
    class Permission {
        +String code
    }
    class Invitation {
        +UUID id
        +String email
        +DateTime expiresAt
        +InvitationStatus status
        +accept(user) Membership
        +revoke()
    }
    class ServiceIdentity {
        +UUID id
        +String name
    }
    class TenantContext {
        +UUID tenantId
        +UUID correlationId
        +Actor actor
    }
    class AuthorizationService {
        +can(ctx, permission, resource) bool
        +requireTenant(ctx, resource)
    }
    Organization "1" --> "*" Membership
    User "1" --> "*" Membership
    Role "1" --> "*" Membership
    Role "*" --> "*" Permission
    Organization "1" --> "*" Invitation
    Organization "1" --> "*" ServiceIdentity
    AuthorizationService ..> TenantContext : uses
    AuthorizationService ..> Role : checks
```

## U2.2 Conversation core (M01, M03)

```mermaid
classDiagram
    class Conversation {
        +UUID id
        +UUID organizationId
        +ConversationStatus status
        +OwnerType owner
        +int version
        +appendInbound(msg) Message
        +appendOutbound(msg) Message
        +claim(agent)
        +release()
        +resolve(outcome)
        +reopen()
    }
    class ConversationParticipant {
        +ParticipantRole role
    }
    class ConversationTurn {
        +UUID id
        +int turnNumber
        +TurnStatus status
    }
    class Message {
        +UUID id
        +long sequence
        +MessageKind kind
        +Direction direction
        +Visibility visibility
        +String body
        +DateTime createdAt
    }
    class MessageMediaReference {
        +String storageKey
        +String mimeType
    }
    class ConversationEvent {
        +String type
        +DateTime occurredAt
    }
    class Customer {
        +UUID id
        +String displayName
        +VerificationLevel level
    }
    class CustomerIdentity {
        +String provider
        +String providerIdentityId
    }
    class CustomerConsent {
        +String purpose
        +bool granted
    }
    class ConversationService {
        +start(ctx, channel) Conversation
        +append(ctx, envelope) Message
        +timeline(ctx, id, visibility) List~Message~
    }
    Conversation "1" *-- "*" Message
    Conversation "1" *-- "*" ConversationTurn
    Conversation "1" *-- "*" ConversationEvent
    Conversation "1" *-- "*" ConversationParticipant
    Message "1" o-- "*" MessageMediaReference
    ConversationTurn "1" --> "*" Message : produces
    Customer "1" --> "*" CustomerIdentity
    Customer "1" --> "*" CustomerConsent
    Customer "1" --> "*" Conversation
    ConversationService ..> Conversation : manages
```

## U2.3 Channel management and delivery (M02)

```mermaid
classDiagram
    class ChannelConnection {
        +UUID id
        +String provider
        +String publicKey
        +List~String~ allowedOrigins
        +bool enabled
    }
    class InboundEvent {
        +String providerEventId
        +ProcessingState state
        +DateTime receivedAt
    }
    class OutboundDelivery {
        +UUID id
        +DeliveryState state
        +int attempts
        +String providerMessageId
        +markSent()
        +markDelivered()
        +markFailed(reason)
    }
    class ChannelAdapter {
        <<interface>>
        +verifySignature(req) bool
        +normalize(req) InboundEnvelope
        +send(cmd) ProviderResult
        +parseReceipt(req) DeliveryReceipt
    }
    class WebsiteChatAdapter
    class EmailAdapter
    class MessagingAdapter
    class InboundEnvelope {
        +String eventId
        +UUID tenantId
        +String providerEventId
        +Customer identity
        +MessageContent message
        +DateTime occurredAt
        +UUID correlationId
    }
    class WebhookController {
        +handle(req) HttpResponse
    }
    class DeliveryWorker {
        +dispatch(delivery)
        +retry(delivery)
    }
    ChannelAdapter <|.. WebsiteChatAdapter
    ChannelAdapter <|.. EmailAdapter
    ChannelAdapter <|.. MessagingAdapter
    ChannelConnection "1" --> "*" InboundEvent
    ChannelConnection "1" --> "*" OutboundDelivery
    WebhookController ..> ChannelAdapter : uses
    WebhookController ..> InboundEnvelope : creates
    DeliveryWorker ..> ChannelAdapter : calls
    DeliveryWorker ..> OutboundDelivery : updates
```

## U2.4 AI Conversation Engine: turn orchestration (M04)

```mermaid
classDiagram
    class TurnOrchestrator {
        +runTurn(ctx, turnId) TurnResult
    }
    class ContextBuilder {
        +build(ctx, conv) PromptContext
    }
    class IntentClassifier {
        +classify(text, taxonomy) Intent
    }
    class Planner {
        +nextStep(state) PlannedStep
    }
    class PolicyEngine {
        +evaluate(ctx, step) PolicyDecision
        +shouldEscalate(state) bool
    }
    class ResponseGenerator {
        +generate(state) Draft
    }
    class OutputGuard {
        +check(draft, evidence) GuardResult
    }
    class AgentExecution {
        +UUID id
        +String modelName
        +int latencyMs
        +Outcome outcome
        +Map decisionMetadata
    }
    class AgentVersion {
        +UUID id
        +allowsTool(name) bool
    }
    class ModelProvider {
        <<interface>>
        +generateResponse(input, schema) ModelOutput
        +streamResponse(input) Stream
        +classify(input, taxonomy) Label
        +embed(texts) List~Vector~
    }
    TurnOrchestrator --> ContextBuilder
    TurnOrchestrator --> IntentClassifier
    TurnOrchestrator --> Planner
    TurnOrchestrator --> PolicyEngine
    TurnOrchestrator --> ResponseGenerator
    TurnOrchestrator --> OutputGuard
    TurnOrchestrator --> AgentExecution : records
    TurnOrchestrator ..> AgentVersion : runs on
    Planner ..> ModelProvider
    ResponseGenerator ..> ModelProvider
    IntentClassifier ..> ModelProvider
```

## U2.4b Agent configuration and versions (M19)

```mermaid
classDiagram
    class AgentConfiguration {
        +UUID id
        +String name
        +publish(draft) AgentVersion
    }
    class AgentVersion {
        +UUID id
        +int number
        +String instructions
        +bool immutable
        +allowsTool(name) bool
    }
    class AgentDeployment {
        +UUID channelConnectionId
        +activate(version)
        +rollback()
    }
    class AgentPolicy {
        +String rule
        +PolicyAction action
    }
    class ModelConfiguration {
        +String model
        +float temperature
        +int maxTokens
    }
    class ToolVersion
    class KnowledgeSource
    AgentConfiguration "1" --> "*" AgentVersion
    AgentVersion "1" --> "*" AgentDeployment
    AgentVersion "1" --> "*" AgentPolicy
    AgentVersion --> ModelConfiguration
    AgentVersion "*" --> "*" ToolVersion : allowlist
    AgentVersion "*" --> "*" KnowledgeSource : assigned
```

## U2.5 Knowledge and retrieval (M05)

```mermaid
classDiagram
    class KnowledgeSource {
        +UUID id
        +SourceType type
        +SourceState state
        +register()
        +delete()
    }
    class Document {
        +UUID id
        +String title
    }
    class DocumentVersion {
        +UUID id
        +String contentHash
        +IngestionState state
        +String storageKey
    }
    class DocumentChunk {
        +UUID id
        +int ordinal
        +String text
        +Map metadata
    }
    class IngestionJob {
        +UUID id
        +JobState state
        +int attempts
        +run()
        +retry()
    }
    class Parser {
        <<interface>>
        +parse(file) ParsedDocument
    }
    class Chunker {
        +chunk(doc) List~DocumentChunk~
    }
    class Embedder {
        <<interface>>
        +embed(chunks) List~Vector~
    }
    class VectorIndex {
        <<interface>>
        +upsert(tenantId, chunks, vectors)
        +search(tenantId, vector, filter, k) List~Hit~
        +deleteBySource(tenantId, sourceId)
    }
    class RetrievalService {
        +retrieve(ctx, query, sources, k) List~Passage~
    }
    class RetrievalRun {
        +int resultCount
        +int latencyMs
    }
    class Passage {
        +String text
        +UUID sourceId
        +float score
    }
    KnowledgeSource "1" --> "*" Document
    Document "1" --> "*" DocumentVersion
    DocumentVersion "1" --> "*" DocumentChunk
    KnowledgeSource "1" --> "*" IngestionJob
    IngestionJob ..> Parser
    IngestionJob ..> Chunker
    IngestionJob ..> Embedder
    IngestionJob ..> VectorIndex
    RetrievalService ..> VectorIndex
    RetrievalService ..> Embedder
    RetrievalService --> RetrievalRun : logs
    RetrievalService --> Passage : returns
```

## U2.6 Tools: registry and execution (M06)

```mermaid
classDiagram
    class ToolDefinition {
        +String name
        +String description
    }
    class ToolVersion {
        +int version
        +JsonSchema inputSchema
        +JsonSchema outputSchema
        +RiskLevel risk
        +String requiredPermission
        +Duration timeout
        +RetryPolicy retry
    }
    class ToolRegistry {
        +resolve(agentVersion, name) ToolVersion
    }
    class ToolExecutionService {
        +execute(invocation) ToolResult
        -validate(invocation)
        -authorize(ctx, tool)
        -redact(result)
    }
    class ToolExecution {
        +UUID id
        +String idempotencyKey
        +ExecStatus status
        +Map redactedArguments
        +DateTime startedAt
    }
    class ActionApproval {
        +ApprovalStatus status
        +UUID approverId
    }
    class Connector {
        <<interface>>
    }
    ToolDefinition "1" --> "*" ToolVersion
    ToolRegistry ..> ToolVersion
    ToolExecutionService ..> ToolRegistry
    ToolExecutionService --> ToolExecution : persists
    ToolExecution "1" --> "0..1" ActionApproval
    ToolExecutionService ..> Connector
```

## U2.6b Integrations and connectors (M15)

```mermaid
classDiagram
    class Connector {
        <<interface>>
        +call(operation, args, secretRef) ConnectorResult
        +healthCheck() Health
    }
    class CommerceConnector
    class CrmConnector
    class ConnectorError {
        +ErrorCategory category
        +bool retryable
    }
    class Integration {
        +UUID id
        +Health health
        +SecretRef credentialRef
    }
    class SecretManager {
        <<interface>>
        +resolve(ref) Secret
    }
    class ToolVersion {
        +String name
        +int version
    }
    Connector <|.. CommerceConnector
    Connector <|.. CrmConnector
    Connector ..> ConnectorError : raises
    Integration --> SecretManager : via ref
    ToolVersion --> Integration : backed by
    Connector ..> Integration : configured by
```

## U2.7 Human handoff and tickets (M10, M11, M13)

```mermaid
classDiagram
    class HandoffEvent {
        +UUID id
        +ReasonCode reason
        +Outcome outcome
        +DateTime requestedAt
    }
    class HandoffBundle {
        +String summary
        +List~Message~ transcript
        +List~ToolExecution~ toolOutcomes
        +List~Citation~ citations
        +VerificationLevel verification
    }
    class HandoffService {
        +request(ctx, conv, reason) HandoffEvent
        +prepareBundle(conv, viewerPermissions) HandoffBundle
    }
    class SupportQueue {
        +String name
        +enqueue(item)
        +claim(item, agent)
    }
    class Assignment {
        +int version
        +AssignmentStatus status
    }
    class SupportAgent {
        +UUID id
        +Set~UUID~ queueIds
    }
    class Ticket {
        +UUID id
        +TicketStatus status
        +Priority priority
        +String category
        +DateTime dueAt
        +changeStatus(s, by)
        +link(conversation)
    }
    class TicketComment {
        +String body
        +bool internal
    }
    class TicketStatusHistory {
        +TicketStatus from
        +TicketStatus to
        +DateTime at
    }
    class RoutingRule {
        +int priority
        +Condition condition
        +matches(item) bool
    }
    class SlaPolicy {
        +Duration responseTarget
        +Duration resolutionTarget
    }
    class EscalationPolicy
    HandoffService --> HandoffEvent : creates
    HandoffEvent --> HandoffBundle
    HandoffEvent "1" --> "0..1" Assignment
    SupportQueue "1" --> "*" Assignment
    SupportAgent "1" --> "*" Assignment
    Ticket "1" *-- "*" TicketComment
    Ticket "1" *-- "*" TicketStatusHistory
    RoutingRule --> SupportQueue : targets
    SlaPolicy "1" --> "*" EscalationPolicy
    Ticket ..> SlaPolicy
```

## U2.8 Voice and speech (M07, M08, M09)

```mermaid
classDiagram
    class VoiceSession {
        +UUID id
        +VoiceState state
        +DateTime startedAt
        +start()
        +end(reason)
        +reconnect()
        +onBargeIn()
    }
    class VoiceSessionEvent {
        +String type
        +DateTime at
    }
    class MediaTransport {
        <<interface>>
        +connect(credentials)
        +sendAudio(frame)
        +close()
    }
    class WebRtcTransport
    class WebSocketTransport
    class SpeechProvider {
        <<interface>>
        +openStream(cfg) SpeechStream
    }
    class SttEngine {
        <<interface>>
        +transcribe(stream) Stream~TranscriptEvent~
    }
    class TtsEngine {
        <<interface>>
        +synthesize(text, voice) Stream~Audio~
        +cancel()
    }
    class SpeechToSpeechEngine {
        <<interface>>
        +open(session) RealtimeSession
    }
    class SpeechConfiguration {
        +String language
        +String voice
        +Strategy strategy
    }
    class TranscriptSegment {
        +long sequence
        +SegmentState state
        +float confidence
        +String text
    }
    class TranscriptSynchronizer {
        +onPartial(seg)
        +onFinal(seg) Message
        +onInterrupted(offset)
    }
    VoiceSession "1" --> "*" VoiceSessionEvent
    VoiceSession "1" --> "*" TranscriptSegment
    VoiceSession --> SpeechConfiguration
    VoiceSession ..> MediaTransport
    MediaTransport <|.. WebRtcTransport
    MediaTransport <|.. WebSocketTransport
    SpeechProvider ..> SttEngine
    SpeechProvider ..> TtsEngine
    SpeechProvider ..> SpeechToSpeechEngine
    TranscriptSynchronizer --> TranscriptSegment
    TranscriptSynchronizer ..> VoiceSession
```

## U2.9 Workflow automation (M12) and notifications (M14)

```mermaid
classDiagram
    class WorkflowDefinition {
        +UUID id
        +String name
    }
    class WorkflowVersion {
        +int number
        +Trigger trigger
        +List~Step~ steps
        +bool immutable
    }
    class WorkflowRun {
        +UUID id
        +RunState state
        +int currentStep
        +advance()
        +suspend()
        +fail(reason)
    }
    class WorkflowStepRun {
        +int attempts
        +StepState state
        +String idempotencyKey
    }
    class Step {
        <<interface>>
        +execute(ctx) StepResult
        +isIdempotent() bool
    }
    class ToolStep
    class ApprovalStep
    class NotifyStep
    class ConditionStep
    class WorkflowEngine {
        +onEvent(event)
        +resume(runId)
        +retry(stepRun)
    }
    class Notification {
        +NotificationStatus status
    }
    class NotificationTemplate {
        +String name
        +String body
    }
    WorkflowDefinition "1" --> "*" WorkflowVersion
    WorkflowVersion "1" --> "*" WorkflowRun
    WorkflowRun "1" *-- "*" WorkflowStepRun
    Step <|.. ToolStep
    Step <|.. ApprovalStep
    Step <|.. NotifyStep
    Step <|.. ConditionStep
    WorkflowEngine --> WorkflowRun
    NotifyStep ..> Notification
    Notification --> NotificationTemplate
```

## U2.10 Security, audit, usage and evaluation (M16, M17, M20)

```mermaid
classDiagram
    class AuditEvent {
        +UUID id
        +String action
        +Actor actor
        +UUID tenantId
        +UUID correlationId
        +Map redactedDetails
        +DateTime at
    }
    class AuditService {
        +record(event)
        +query(ctx, filter) List~AuditEvent~
    }
    class Redactor {
        +redact(payload, policy) Payload
    }
    class UsageRecord {
        +String meter
        +decimal quantity
        +UUID agentVersionId
        +UUID channelId
    }
    class QuotaService {
        +check(ctx, meter) bool
    }
    class RetentionPolicy {
        +DataClass dataClass
        +Duration keepFor
    }
    class SecurityEvent {
        +String kind
        +Severity severity
    }
    class EvaluationDataset {
        +List~EvalCase~ cases
    }
    class EvaluationRun {
        +UUID agentVersionId
        +RunStatus status
        +execute()
    }
    class EvaluationResult {
        +Map scores
        +bool critical
    }
    class ReleaseGate {
        +decide(run) GateDecision
    }
    class AgentRelease {
        +String version
        +DateTime releasedAt
    }
    class MetricEvent {
        +String name
        +Map safeLabels
    }
    AuditService ..> Redactor
    AuditService --> AuditEvent
    QuotaService ..> UsageRecord
    EvaluationDataset "1" --> "*" EvaluationRun
    EvaluationRun "1" --> "*" EvaluationResult
    ReleaseGate ..> EvaluationRun
    ReleaseGate --> AgentRelease : allows
```

## U2.11 Design patterns applied

```mermaid
classDiagram
    class Port {
        <<interface>>
    }
    class Adapter
    class Strategy {
        <<interface>>
    }
    class State {
        <<interface>>
    }
    class Repository~T~ {
        <<interface>>
        +find(ctx, id) T
        +save(ctx, entity)
    }
    class TenantAwareRepository~T~ {
        -applyTenantFilter(ctx, query)
    }
    class OutboxPublisher {
        +enqueue(event)
        +relay()
    }
    class IdempotencyStore {
        +seen(key) bool
        +remember(key, result)
    }
    class CircuitBreaker {
        +allow() bool
        +recordSuccess()
        +recordFailure()
    }
    Port <|.. Adapter : Adapter pattern for providers
    Strategy <|.. Adapter : Strategy for STT TTS S2S
    Repository <|.. TenantAwareRepository : Decorator and Template Method
    State <|.. Adapter : State for conversation and delivery
    OutboxPublisher ..> Repository
    Adapter ..> CircuitBreaker
    Adapter ..> IdempotencyStore
```
