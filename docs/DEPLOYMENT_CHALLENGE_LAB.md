# Netiks Store Deployment Challenge Lab

## 1. Lab Title

Production-Style Deployment Challenge for Netiks Store on AWS and Azure

## 2. Lab Purpose

This lab is designed to teach interns how to deploy a real multi-service application using a production-style pattern while staying within a controlled student budget.

Every intern will deploy the same project, follow the same target architecture, and submit the same class of evidence. Interns may collaborate during learning, but each intern must complete and submit an individual deployment in their own cloud account or assigned subscription.

This lab is intentionally opinionated. The goal is not to let every intern invent a different deployment style. The goal is to make everyone practice the same baseline standard so that deployments can be reviewed fairly and improved in later labs.

## 3. What They Are Deploying

The project to deploy is the Netiks Store repository.

The relevant application components are:

- `apps/web` for the Next.js frontend
- `apps/gateway` for the FastAPI gateway
- `services/identity-service`
- `services/vendor-service`
- `services/catalog-service`
- `services/media-service`
- `services/admin-service`
- PostgreSQL
- Redis

The local reference architecture is defined in [README.md](/Users/woron/Documents/netiks-store/README.md) and [docker-compose.yml](/Users/woron/Documents/netiks-store/docker-compose.yml).

## 4. Standard Deployment Pattern

All interns must use the same base deployment pattern:

- One Linux virtual machine
- Docker Engine and Docker Compose on the VM
- The Netiks Store services deployed as containers on that VM
- One reverse proxy in front of the application
- One public entry point for the application
- PostgreSQL running in a container on the same VM for this lab
- Redis running in a container on the same VM for this lab
- Persistent Docker volumes for PostgreSQL data and uploaded media
- Container images stored in a cloud container registry
- Source code stored in GitHub
- Secrets stored outside the GitHub repository

This is the required standard for this lab because it is:

- close enough to real production workflows to teach useful habits
- affordable for interns
- easy to troubleshoot
- consistent across AWS and Azure
- a strong foundation for later labs involving CI/CD, monitoring, scaling, backups, and storage migration

## 5. Why This Pattern Is Recommended

This project is a microservice application, but it is still a training project. Using managed Kubernetes, managed PostgreSQL, service mesh, private networking across many subnets, and advanced autoscaling would increase complexity and cost too early.

For this stage, interns should learn these fundamentals first:

- VM provisioning
- network security rules
- container registry usage
- Docker Compose deployment
- reverse proxy setup
- domain or public-IP exposure
- environment variable and secret management
- health checks
- log inspection
- deployment documentation
- least-privilege access for review

Later labs can build on this same deployment and introduce:

- CI/CD pipelines
- managed databases
- object storage for media
- TLS hardening
- backup automation
- observability stacks
- blue/green or rolling deployment patterns

## 6. Cloud Mapping

Each cloud team must implement the same architecture using the provider services below.

| Function | AWS interns | Azure interns |
|---|---|---|
| Source repository | GitHub | GitHub |
| Linux VM | EC2 | Azure Virtual Machine |
| Security boundary | Security Group | Network Security Group |
| Container registry | Amazon ECR | Azure Container Registry |
| Identity for review access | IAM User | Microsoft Entra ID user or guest user with RBAC |
| Monitoring baseline | CloudWatch agent optional | Azure Monitor agent optional |
| Public access | Elastic IP or public IP | Public IP |

## 7. Cost Guardrails

Interns must optimize for low but realistic cost.

Required cost rules:

- Use one small Linux VM only.
- Do not create a Kubernetes cluster.
- Do not create a managed PostgreSQL service for this lab.
- Do not create a load balancer unless explicitly approved.
- Do not create more than one production VM.
- Do not leave unused disks, IPs, snapshots, or old container images lying around.
- Shut down and delete unused resources after grading when instructed.

Recommended sizing:

- AWS: start with a small burstable Linux EC2 instance such as `t3.small` or similar low-cost equivalent if available in the chosen region.
- Azure: start with a small burstable Linux VM in the B-series such as `B1ms` or another low-cost equivalent if available in the chosen region.
- Disk: use the smallest practical SSD that still supports the OS, Docker images, logs, and PostgreSQL data.

Notes on pricing:

- AWS states that T3 instances are positioned as a low-cost burstable option, with pricing starting from very low hourly rates depending on size and region.
- Azure describes B-series VMs as economical burstable VMs and shows entry pricing for that family starting from a low monthly level, though the actual bill depends on region and selected size.
- Amazon ECR pricing is usage-based, so interns should keep image count and image size under control.
- Azure Container Registry pricing varies by tier; interns should use the lowest tier that supports the lab.

Before creating resources, each intern must estimate their monthly cost using the provider calculator or pricing page for their selected region and record that estimate in their submission.

## 8. Required Target Architecture

Every submission must include this logical layout:

1. GitHub repository containing the project and deployment notes.
2. Cloud container registry containing the application images.
3. One Ubuntu Linux VM.
4. Docker and Docker Compose installed on that VM.
5. Reverse proxy container or host-level reverse proxy routing traffic to:
   - frontend web service
   - API gateway
6. Backend services deployed as containers.
7. PostgreSQL container with persistent storage.
8. Redis container.
9. Persistent volume for media uploads.
10. Security rules allowing only the minimum required inbound traffic.

Recommended inbound ports:

- `22` for SSH, restricted to trusted IPs where possible
- `80` for HTTP
- `443` for HTTPS if domain and TLS are configured

Ports like `8000`, `8001`, `8002`, `8003`, `8004`, `8005`, `5432`, and `6379` must not be exposed publicly unless there is a documented temporary testing reason and that reason is removed before final submission.

## 9. Non-Negotiable Standards

Every intern must meet these baseline standards:

- The application must be deployed from the GitHub project, not copied manually into the VM.
- The repo must contain deployment documentation.
- The VM must not run everything as an undifferentiated manual shell session with undocumented commands.
- Secrets must not be committed into GitHub.
- The deployment must be reproducible.
- The public application must load successfully.
- The API gateway health endpoint must respond successfully.
- Containers must restart automatically if the VM reboots.
- The intern must be able to explain the purpose of each cloud resource they created.
- All resources must be tagged or named consistently.

## 10. Naming Standard

Each intern must use this naming pattern:

- Project prefix: `netiks`
- Environment: `dev`
- Cloud owner suffix: `<firstname>-<lastname>` or another approved unique ID

Examples:

- `netiks-dev-jane-doe-vm`
- `netiks-dev-jane-doe-rg`
- `netiks-dev-jane-doe-ecr`
- `netiks-dev-jane-doe-acr`

Required tags or labels:

- `Project=NetiksStore`
- `Environment=Dev`
- `Owner=<intern-name>`
- `Lab=DeploymentChallenge`

## 11. Required Tasks

Each intern must complete the following tasks.

### Task 1: Repository preparation

- Fork or clone the Netiks Store repository.
- Create a branch for deployment-related work if required by the team workflow.
- Add a deployment document in the repo describing exactly how the deployment works.
- Add any deployment-specific files needed for the cloud target.

### Task 2: Container image preparation

- Build the application container images.
- Push the images to the assigned cloud registry.
- Use clear image tags.

Minimum tagging standard:

- `latest`
- one unique version tag such as a commit SHA or date-based tag

### Task 3: VM provisioning

- Provision one Linux VM.
- Secure SSH access.
- Update the OS packages.
- Install Docker and Docker Compose.
- Install Git.
- Prepare a working deployment directory on the VM.

### Task 4: Runtime configuration

- Create a production-style `.env` file on the VM.
- Configure all required application variables.
- Keep secrets out of the repository.
- Document where secrets are stored and how they are applied.

### Task 5: Reverse proxy and networking

- Put the application behind a reverse proxy.
- Route browser traffic cleanly to the frontend and API.
- Expose only required public ports.
- Ensure the deployment is reachable using a public IP or domain.

### Task 6: Application deployment

- Pull the project or deployment files from GitHub onto the VM.
- Pull images from the registry or build them on the VM if justified.
- Start the stack with Docker Compose.
- Verify that all required services are healthy.

### Task 7: Validation

- Load the homepage successfully.
- Verify the API gateway health route.
- Verify at least one application flow, such as login, store retrieval, catalog listing, or media retrieval.
- Capture logs showing successful service startup.

### Task 8: Operational readiness

- Configure container restart policies.
- Document how to restart the application after failure.
- Document how to inspect logs.
- Document how to update the deployment to a newer image tag.
- Document at least one rollback approach.

### Task 9: Review access for instructor

- Create instructor inspection access using the required least-privilege model for the cloud platform.
- Test that the account can view the deployed resources.
- Share the access details securely using the approved class process.

## 12. Instructor Review Access Requirements

The goal of review access is inspection, not daily administration.

### 12.1 AWS interns

Each AWS intern must create a dedicated IAM user for instructor review.

Required minimum standard:

- Create one IAM user named with the pattern `netiks-review-<intern-id>`.
- Enable AWS Management Console access for that user.
- Assign a strong password and share it through the approved secure channel.
- Require password reset on first login only if that does not block the instructor review workflow.
- Attach a read-only policy set.

Recommended policy choice for this lab:

- `ReadOnlyAccess`

Recommended extras if needed for better inspection:

- billing view access only if the account owner has intentionally enabled IAM access to billing and wants cost review included

The review user must be able to inspect:

- EC2 instance
- security group
- ECR repository
- CloudWatch logs if used
- IAM resources related to the deployment
- resource tags

The review user must not have permissions to:

- terminate resources
- change networking
- rotate secrets
- delete the registry

### 12.2 Azure interns

Each Azure intern must create instructor review access in Azure using Microsoft Entra ID and RBAC.

Required minimum standard:

- Create a dedicated instructor user in the tenant or invite the instructor as a guest user.
- Assign the `Reader` role at the resource group scope used for this lab.

Recommended additional roles if required for visibility:

- `Monitoring Reader`
- `Log Analytics Reader`

The review identity must be able to inspect:

- resource group
- VM
- networking resources
- Azure Container Registry
- monitoring resources if used
- tags

The review identity must not be able to:

- delete resources
- change network rules
- change secrets
- stop the deployment without approval

## 13. Submission Deliverables

Each intern must submit all of the following:

1. GitHub repository link
2. Public application URL or public IP
3. Public API health endpoint URL
4. Architecture diagram
5. Cost estimate for one month in the chosen region
6. Screenshot evidence of:
   - cloud resources
   - running containers
   - successful homepage load
   - successful API health check
7. Deployment document in the repo
8. Review-access details shared through the approved secure process
9. Short runbook covering:
   - deploy
   - restart
   - inspect logs
   - update version
   - rollback
10. One short reflection section:
   - what worked
   - what failed
   - what would be improved next

## 14. Required Repository Documentation

Each intern must add a deployment document in their repo with the following sections:

- Overview
- Architecture
- Cloud resources created
- Deployment steps
- Environment variables used
- Security decisions
- Cost estimate
- Validation evidence
- Troubleshooting notes
- Rollback steps
- Cleanup steps

Suggested filename:

- `docs/DEPLOYMENT_REPORT.md`

## 15. Acceptance Criteria

An intern passes this lab only if all the following are true:

- The application is reachable from the internet.
- The frontend loads successfully.
- The gateway endpoint responds successfully.
- The deployment uses the required single-VM containerized pattern.
- The deployment is documented clearly enough that another person can follow it.
- Review access is created correctly.
- The intern can explain the cost of the resources they chose.
- Public exposure is limited to the necessary ports.
- Secrets are not stored in the repository.
- The deployment can survive a VM reboot without manual recreation.

## 16. Grading Rubric

Total: 100 points

- Architecture compliance: 20 points
- Correctness of deployment: 20 points
- Security hygiene: 15 points
- Cost awareness and restraint: 10 points
- Documentation quality: 15 points
- Operational readiness and troubleshooting: 10 points
- Review access setup: 10 points

Automatic point losses:

- minus 20 if secrets are committed to the repository
- minus 15 if databases or internal service ports are exposed publicly
- minus 15 if the instructor cannot inspect resources due to bad review access setup
- minus 10 if no cost estimate is provided

## 17. Stretch Goals

These are optional and should only be attempted after the core lab is complete:

- configure HTTPS with a real domain
- move media storage to S3 or Azure Blob Storage
- add GitHub Actions for image build and deployment
- add basic monitoring dashboards
- add backup automation for PostgreSQL
- add image vulnerability scanning

## 18. What Success Looks Like

At the end of this lab, every intern should be able to:

- explain the deployment architecture clearly
- build and publish container images
- provision and secure a Linux VM
- deploy a multi-container application using Docker Compose
- expose the application safely
- document operational procedures
- provide least-privilege review access
- reason about deployment cost instead of deploying blindly

## 19. Suggested Instructor Notes

For consistency across the cohort, instruct interns not to optimize for cleverness. They should optimize for:

- clarity
- reproducibility
- security basics
- cost control
- ability to explain their choices

If an intern wants to use a more advanced design, they should first complete the required standard design and get it working end to end.

## 20. Recommended References

- Project overview: [README.md](/Users/woron/Documents/netiks-store/README.md)
- Practical system guide: [PROJECT_DOCUMENTATION.md](/Users/woron/Documents/netiks-store/docs/PROJECT_DOCUMENTATION.md)
- Technical architecture: [TECHNICAL_PLAN.md](/Users/woron/Documents/netiks-store/docs/TECHNICAL_PLAN.md)
- Local baseline: [docker-compose.yml](/Users/woron/Documents/netiks-store/docker-compose.yml)
