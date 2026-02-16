# OpenAI Frontier Security Readiness Questionnaire

## Overview

**Date:** February 15, 2026
**Purpose:** Security readiness assessment for OpenAI Frontier partnership

### What is OpenAI Frontier?

OpenAI Frontier is an end-to-end enterprise platform launched on February 5, 2026, designed for building, deploying, and managing AI agents that can automate core workflows at scale. The platform:

- Acts as an intelligence layer integrating disparate systems and data
- Supports OpenAI-built agents, custom enterprise agents, and third-party agents (Google, Microsoft, Anthropic)
- Provides identity management and permission controls for each AI agent
- Meets leading compliance standards: SOC 2 Type II, ISO/IEC 27001, 27017, 27018, 27701, and CSA STAR

**Initial enterprise customers:** Uber, State Farm, Intuit, Thermo Fisher Scientific

**Key partners:** Abridge, Clay, Ambience, Decagon, Harvey, Sierra, Snowflake

---

## Security Assessment Framework

This questionnaire is organized by security domain to help you prepare answers for OpenAI's partnership onboarding process.

---

## 1. Identity & Access Management (IAM)

### Questions OpenAI Frontier May Ask:

**Microsoft Entra ID (formerly Azure AD)**
- [ ] Do you use Microsoft Entra ID for identity management?
- [ ] What is your Entra ID tenant configuration (single/multi-tenant)?
- [ ] Do you use Entra ID Conditional Access policies?
- [ ] Are you using Entra ID Premium P1 or P2?

**Role-Based Access Control (RBAC)**
- [ ] Do you have RBAC implemented across your organization?
- [ ] What are your standard role definitions (e.g., Admin, User, Developer, Auditor)?
- [ ] How do you assign and review role permissions?
- [ ] Do you follow the Principle of Least Privilege?

**Authentication & Authorization**
- [ ] Do you support Multi-Factor Authentication (MFA)?
- [ ] Is MFA enforced for all privileged accounts?
- [ ] What authentication methods do you support (password, passwordless, biometric, hardware tokens)?
- [ ] Do you use Single Sign-On (SSO)?
- [ ] What is your password policy (complexity, rotation, history)?

**Identity Lifecycle Management**
- [ ] How do you provision new user accounts?
- [ ] How do you deprovision accounts when employees leave?
- [ ] Do you have automated identity lifecycle workflows?
- [ ] How frequently do you review access rights?

### Your Organization's Answers:

**Entra ID Configuration:**
```
[Your answer here]
```

**RBAC Implementation:**
```
[Your answer here]
```

**Authentication Methods:**
```
[Your answer here]
```

**Identity Lifecycle:**
```
[Your answer here]
```

---

## 2. Data Classification & Protection

### Questions OpenAI Frontier May Ask:

**Data Classification Tiers**
- [ ] Do you have a formal data classification policy?
- [ ] What are your data classification tiers? (Common: Public, Internal, Confidential, Highly Confidential/Restricted)
- [ ] How do you label and tag data based on classification?
- [ ] Who is responsible for classifying data?

**Data Protection Controls**
- [ ] What encryption standards do you use for data at rest?
- [ ] What encryption standards do you use for data in transit?
- [ ] Do you use Enterprise Key Management (EKM) or Bring Your Own Key (BYOK)?
- [ ] How do you protect API keys and secrets? (e.g., Azure Key Vault, HashiCorp Vault)

**Data Handling Policies**
- [ ] What types of data will be processed through OpenAI Frontier?
- [ ] Do you process Personally Identifiable Information (PII)?
- [ ] Do you process Protected Health Information (PHI)?
- [ ] Do you process payment card data (PCI)?
- [ ] What is your data retention policy?
- [ ] What is your data deletion/destruction process?

**Data Loss Prevention (DLP)**
- [ ] Do you have DLP solutions in place?
- [ ] Which DLP tools do you use? (e.g., Microsoft Purview, Symantec, Forcepoint)
- [ ] What data types are monitored by DLP?
- [ ] How do you handle DLP policy violations?

### Your Organization's Answers:

**Data Classification Tiers:**
```
Tier 1 (Public):
Tier 2 (Internal):
Tier 3 (Confidential):
Tier 4 (Restricted):
```

**Encryption Standards:**
```
Data at rest:
Data in transit:
Key management:
```

**Sensitive Data Handling:**
```
PII handling:
PHI handling:
PCI compliance:
```

**DLP Implementation:**
```
[Your answer here]
```

---

## 3. Compliance & Certifications

### Questions OpenAI Frontier May Ask:

**Regulatory Requirements**
- [ ] Which regulations apply to your organization? (GDPR, CCPA, HIPAA, SOX, PCI-DSS, etc.)
- [ ] Are you required to have Business Associate Agreements (BAA) for HIPAA?
- [ ] Do you have data sovereignty requirements?
- [ ] Which countries/regions must your data remain in?

**Security Certifications**
- [ ] Does your organization hold SOC 2 Type II certification?
- [ ] Do you hold ISO 27001 certification?
- [ ] What other security certifications do you maintain?
- [ ] When were your certifications last audited?

**Audit & Compliance Monitoring**
- [ ] Do you have an internal audit team?
- [ ] How frequently do you conduct security audits?
- [ ] Do you use compliance monitoring tools?
- [ ] How do you track compliance with security policies?

**eDiscovery Requirements**
- [ ] Do you have eDiscovery requirements?
- [ ] What eDiscovery tools do you use?
- [ ] How long do you retain audit logs?
- [ ] Can you produce time-stamped records of AI interactions?

### Your Organization's Answers:

**Applicable Regulations:**
```
[Your answer here]
```

**Security Certifications:**
```
[Your answer here]
```

**Audit Frequency:**
```
[Your answer here]
```

**eDiscovery Capabilities:**
```
[Your answer here]
```

---

## 4. Workload & Device Management

### Questions OpenAI Frontier May Ask:

**Microsoft Intune / Endpoint Management**
- [ ] Do you use Microsoft Intune for device management?
- [ ] What types of devices are managed? (Windows, macOS, iOS, Android)
- [ ] Do you enforce device compliance policies?
- [ ] What happens when devices fall out of compliance?

**Device Security Policies**
- [ ] Do you require device encryption?
- [ ] Do you enforce screen lock/timeout policies?
- [ ] Do you use Mobile Device Management (MDM)?
- [ ] Do you use Mobile Application Management (MAM)?

**Application Management**
- [ ] How do you deploy and manage applications?
- [ ] Do you have an approved application whitelist?
- [ ] How do you handle shadow IT?
- [ ] Do you use containerization for work apps (e.g., managed app containers)?

**Conditional Access**
- [ ] Do you enforce conditional access based on device compliance?
- [ ] Do you restrict access based on location?
- [ ] Do you use risk-based conditional access?

### Your Organization's Answers:

**Intune Configuration:**
```
[Your answer here]
```

**Device Policies:**
```
[Your answer here]
```

**Application Management:**
```
[Your answer here]
```

**Conditional Access:**
```
[Your answer here]
```

---

## 5. AI Agent Security & Governance

### Questions OpenAI Frontier May Ask:

**Agent Identity & Permissions**
- [ ] How will you assign identities to AI agents in Frontier?
- [ ] What permission model will you use for AI agents?
- [ ] Will each agent have its own service principal/managed identity?
- [ ] How will you implement least privilege for AI agents?

**Agent Guardrails**
- [ ] What operational boundaries will you set for AI agents?
- [ ] How will you prevent agents from accessing unauthorized systems?
- [ ] What approval workflows will be required for agent actions?
- [ ] How will you handle agent errors or policy violations?

**AI Usage Policies**
- [ ] Do you have an AI acceptable use policy?
- [ ] What workflows can AI agents automate?
- [ ] What workflows are off-limits for AI automation?
- [ ] How do you govern AI model selection and usage?

**Human-in-the-Loop**
- [ ] Which agent actions require human approval?
- [ ] How will you implement human oversight for critical operations?
- [ ] What is your escalation process for agent-related issues?

### Your Organization's Answers:

**Agent Identity Management:**
```
[Your answer here]
```

**Guardrails & Boundaries:**
```
[Your answer here]
```

**AI Governance Policy:**
```
[Your answer here]
```

**Human Oversight:**
```
[Your answer here]
```

---

## 6. Network & Infrastructure Security

### Questions OpenAI Frontier May Ask:

**Network Architecture**
- [ ] Do you use network segmentation/VLANs?
- [ ] Do you have a DMZ for external-facing applications?
- [ ] Do you use a Zero Trust Network Architecture?
- [ ] What is your firewall strategy?

**API Security**
- [ ] How do you secure API endpoints?
- [ ] Do you use API gateways?
- [ ] Do you implement rate limiting?
- [ ] How do you authenticate API calls?
- [ ] Where do you store API keys? (Key vault solution)

**Cloud Infrastructure**
- [ ] Which cloud providers do you use? (Azure, AWS, GCP)
- [ ] Do you use Infrastructure as Code (IaC)?
- [ ] How do you secure cloud resources?
- [ ] Do you use Virtual Private Cloud (VPC) / Virtual Network (VNet)?

**Data Residency**
- [ ] Where is your data currently stored (geographic regions)?
- [ ] Do you require in-region processing for compliance?
- [ ] Which regions are acceptable for data storage?
- [ ] Do you need dedicated/isolated infrastructure?

### Your Organization's Answers:

**Network Architecture:**
```
[Your answer here]
```

**API Security:**
```
[Your answer here]
```

**Cloud Infrastructure:**
```
[Your answer here]
```

**Data Residency Requirements:**
```
[Your answer here]
```

---

## 7. Security Monitoring & Incident Response

### Questions OpenAI Frontier May Ask:

**Security Monitoring**
- [ ] What SIEM solution do you use? (e.g., Microsoft Sentinel, Splunk, QRadar)
- [ ] Do you have 24/7 security monitoring?
- [ ] What security events do you log and monitor?
- [ ] How long do you retain security logs?

**Threat Detection**
- [ ] Do you use EDR/XDR solutions?
- [ ] What threat intelligence feeds do you consume?
- [ ] Do you have automated threat detection?
- [ ] How do you detect anomalous AI agent behavior?

**Incident Response**
- [ ] Do you have a formal incident response plan?
- [ ] Do you have a dedicated security operations center (SOC)?
- [ ] What is your incident response time SLA?
- [ ] How do you classify security incidents (P1, P2, P3, P4)?
- [ ] Do you conduct post-incident reviews?

**Vulnerability Management**
- [ ] How frequently do you conduct vulnerability scans?
- [ ] What is your patch management process?
- [ ] What is your SLA for patching critical vulnerabilities?
- [ ] Do you conduct penetration testing? How often?

### Your Organization's Answers:

**SIEM & Monitoring:**
```
[Your answer here]
```

**Threat Detection:**
```
[Your answer here]
```

**Incident Response:**
```
[Your answer here]
```

**Vulnerability Management:**
```
[Your answer here]
```

---

## 8. Vendor & Third-Party Risk Management

### Questions OpenAI Frontier May Ask:

**Vendor Assessment**
- [ ] Do you have a vendor security assessment process?
- [ ] What security requirements do you have for vendors?
- [ ] Do you require vendors to complete security questionnaires?
- [ ] How frequently do you review vendor security posture?

**Third-Party Integrations**
- [ ] What systems will OpenAI Frontier integrate with?
- [ ] How are third-party integrations authenticated?
- [ ] Do you have API governance for third-party connections?
- [ ] How do you monitor third-party access to your systems?

**Contracts & Agreements**
- [ ] Do you require NDAs with vendors?
- [ ] Do you require Data Processing Agreements (DPA)?
- [ ] What are your contract requirements for data ownership?
- [ ] Do you require cyber insurance from vendors?

### Your Organization's Answers:

**Vendor Security Process:**
```
[Your answer here]
```

**Third-Party Integrations:**
```
[Your answer here]
```

**Contract Requirements:**
```
[Your answer here]
```

---

## 9. Training & Awareness

### Questions OpenAI Frontier May Ask:

**Security Awareness Training**
- [ ] Do you provide security awareness training to all employees?
- [ ] How frequently is security training conducted?
- [ ] Do you provide specialized training for AI usage?
- [ ] How do you measure training effectiveness?

**AI-Specific Training**
- [ ] Do users understand how to use AI tools securely?
- [ ] Have you trained users on data classification and what can be shared with AI?
- [ ] Do you have guidelines for prompt engineering security?
- [ ] How do you prevent prompt injection and other AI-specific attacks?

### Your Organization's Answers:

**Security Training Program:**
```
[Your answer here]
```

**AI Usage Training:**
```
[Your answer here]
```

---

## 10. Backup & Disaster Recovery

### Questions OpenAI Frontier May Ask:

**Backup Strategy**
- [ ] What is your backup frequency?
- [ ] Where are backups stored?
- [ ] Are backups encrypted?
- [ ] How long do you retain backups?
- [ ] Do you test backup restoration regularly?

**Business Continuity**
- [ ] Do you have a business continuity plan?
- [ ] What is your Recovery Time Objective (RTO)?
- [ ] What is your Recovery Point Objective (RPO)?
- [ ] Do you have redundant systems/failover?

**Disaster Recovery**
- [ ] Do you have a disaster recovery plan?
- [ ] How frequently do you test DR procedures?
- [ ] Do you have a secondary site/region?

### Your Organization's Answers:

**Backup Configuration:**
```
[Your answer here]
```

**Business Continuity:**
```
RTO:
RPO:
```

**DR Testing:**
```
[Your answer here]
```

---

## Additional Questions to Prepare

### OpenAI Frontier-Specific Questions

1. **What business processes do you plan to automate with AI agents?**
   ```
   [Your answer here]
   ```

2. **Which systems of record will Frontier need to integrate with?**
   ```
   [Your answer here]
   ```

3. **What is your expected scale? (number of agents, users, transactions)**
   ```
   [Your answer here]
   ```

4. **Do you have existing AI/ML initiatives that Frontier will complement?**
   ```
   [Your answer here]
   ```

5. **What are your success metrics for the Frontier deployment?**
   ```
   [Your answer here]
   ```

---

## Action Items

- [ ] Review each security domain and fill in your organization's current state
- [ ] Identify gaps between your current posture and OpenAI Frontier requirements
- [ ] Prioritize remediation efforts for any gaps
- [ ] Prepare documentation and evidence (certifications, policies, architecture diagrams)
- [ ] Schedule internal review with security, compliance, and IT teams
- [ ] Designate a point of contact for OpenAI security discussions

---

## Resources & References

### OpenAI Frontier Documentation
- [Introducing OpenAI Frontier](https://openai.com/index/introducing-openai-frontier/)
- [OpenAI Frontier Enterprise Platform](https://openai.com/business/frontier/)

### OpenAI Security & Compliance
- [Business data privacy, security, and compliance](https://openai.com/business-data/)
- [Security and privacy at OpenAI](https://openai.com/security-and-privacy/)
- [Enterprise privacy at OpenAI](https://openai.com/enterprise-privacy/)
- [Admin Controls, Security, and Compliance](https://help.openai.com/en/articles/11509118-admin-controls-security-and-compliance-in-apps-enterprise-edu-and-business)

### Security Best Practices
- [OpenAI API Security: How to Deploy Safely in Production](https://www.reco.ai/hub/openai-api-security)
- [OpenAI safety best practices](https://www.eesel.ai/blog/openai-safety-best-practices)
- [Safety best practices | OpenAI API](https://developers.openai.com/api/docs/guides/safety-best-practices)

### Microsoft Entra ID & Azure Integration
- [Microsoft Entra ID authentication with Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/managed-identity?view=foundry-classic)
- [Role-based access control for Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/role-based-access-control?view=foundry-classic)
- [Configure keyless authentication with Microsoft Entra ID](https://learn.microsoft.com/en-us/azure/ai-foundry/foundry-models/how-to/configure-entra-id?view=foundry-classic)

### Compliance & Regulatory
- [AI Risk & Compliance 2026: Enterprise Governance Overview](https://secureprivacy.ai/blog/ai-risk-compliance-2026)
- [AI Security Standards: Key Frameworks for 2026](https://www.sentinelone.com/cybersecurity-101/data-and-ai/ai-security-standards/)

### Partnership Information
- [OpenAI launches new enterprise platform](https://www.cnbc.com/2026/02/05/open-ai-frontier-enterprise-customers.html)
- [OpenAI Frontier Platform Guide](https://almcorp.com/blog/openai-frontier-enterprise-ai-agent-platform-guide/)

---

**Document Version:** 1.0
**Last Updated:** February 15, 2026
**Next Review Date:** [Set based on your review cycle]
