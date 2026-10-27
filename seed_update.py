import os
from datetime import date, datetime
from pathlib import Path
from app import create_app
from extensions import db
from models import Admin, Certificate, CompanySettings, Intern, Internship, Mentor, MentorEvaluation, Project
from services.certificate_service import generate_certificate_pdf, generate_qr_png

app = create_app()

with app.app_context():
    upload_root = Path(app.config['UPLOAD_FOLDER'])
    qr_dir = upload_root / 'qr'
    cert_dir = upload_root / 'certificates'
    qr_dir.mkdir(parents=True, exist_ok=True)
    cert_dir.mkdir(parents=True, exist_ok=True)
    frontend = app.config['FRONTEND_URL'].rstrip('/')

    mentor = Mentor.query.first()
    company = CompanySettings.query.first()

    # 1. First, check if PSM001 exists and migrate to PSMI012
    old_intern = Intern.query.filter_by(intern_id='PSM001').first()
    if old_intern:
        print('Migrating existing PSM001 to PSMI012...')
        old_intern.intern_id = 'PSMI012'
        old_intern.photo_path = str((upload_root / 'photos' / 'PSMI012.jpeg').resolve())
        # Update certificate if exists
        old_cert = Certificate.query.filter_by(intern_pk=old_intern.id).first()
        if old_cert:
            old_cert.certificate_id = 'PSM-CERT-PSMI012'
            old_cert.qr_payload = f'{frontend}/verify?id=PSM-CERT-PSMI012'
        db.session.commit()
        print('PSM001 successfully updated to PSMI012!')

    seed_interns = [
        {
            'intern_id': 'PSMI012',
            'full_name': 'Karthikeyan K',
            'email': 'karthikalidasan14@gmail.com',
            'domain': 'Full Stack Development',
            'photo_filename': 'PSMI012.jpeg',
            'cert_id': 'PSM-CERT-PSMI012',
            'internship': {
                'start_date': date(2025, 10, 6),
                'end_date': date(2026, 4, 6),
                'duration_label': '6 October 2025 - 6 April 2026',
                'status': 'Completed',
                'organisation': 'Problem Solving Mind',
            },
            'project': {
                'title': 'PSM Internship Certificate Verification Platform',
                'description': 'A public verification portal and admin console for intern profiles, project records, mentor evaluations and tamper-evident certificates with ID cards.',
                'technologies': 'React, Vite, Flask, SQLite/MySQL, ReportLab, QR codes',
                'github_url': 'https://github.com/problemsolvingmind/internship-verification-platform',
                'live_url': frontend,
                'status': 'Completed',
            },
            'evaluation': {
                'technical_skills': 19,
                'problem_solving': 18,
                'code_quality': 19,
                'communication': 18,
                'teamwork': 18,
                'feedback': 'Outstanding dedication, excellent full stack problem solving abilities, and high code quality delivered throughout the internship.',
            },
        },
        {
            'intern_id': 'PSMI013',
            'full_name': 'Divya K',
            'email': 'divya.k@problemsolvingmind.org',
            'domain': 'Data Science & Machine Learning',
            'photo_filename': 'PSMI013.jpeg',
            'cert_id': 'PSM-CERT-PSMI013',
            'internship': {
                'start_date': date(2025, 9, 15),
                'end_date': date(2026, 3, 15),
                'duration_label': '15 September 2025 - 15 March 2026',
                'status': 'Completed',
                'organisation': 'Problem Solving Mind',
            },
            'project': {
                'title': 'Predictive Analytics & Student Performance Engine',
                'description': 'Machine learning model pipelines analyzing student code submission benchmarks, automated grading metrics, and early risk detection.',
                'technologies': 'Python, Scikit-Learn, Pandas, FastAPI, PostgreSQL',
                'github_url': 'https://github.com/problemsolvingmind/student-analytics-engine',
                'live_url': frontend,
                'status': 'Completed',
            },
            'evaluation': {
                'technical_skills': 18,
                'problem_solving': 19,
                'code_quality': 18,
                'communication': 17,
                'teamwork': 18,
                'feedback': 'Exceptional analytical thinking, strong grasp of ML pipelines, and clear presentation of complex performance data.',
            },
        },
        {
            'intern_id': 'PSMI014',
            'full_name': 'Rahul Sharma',
            'email': 'rahul.sharma@problemsolvingmind.org',
            'domain': 'Cloud & DevOps Engineering',
            'photo_filename': 'PSMI014.jpeg',
            'cert_id': 'PSM-CERT-PSMI014',
            'internship': {
                'start_date': date(2025, 11, 1),
                'end_date': date(2026, 5, 1),
                'duration_label': '1 November 2025 - 1 May 2026',
                'status': 'Completed',
                'organisation': 'Problem Solving Mind',
            },
            'project': {
                'title': 'Automated Cloud CI/CD & Infrastructure as Code',
                'description': 'Zero-downtime deployment pipelines with Docker, Kubernetes clustering, Terraform provisioning, and real-time observability dashboards.',
                'technologies': 'Docker, Kubernetes, AWS, Terraform, GitHub Actions, Prometheus',
                'github_url': 'https://github.com/problemsolvingmind/cloud-infra-pipeline',
                'live_url': frontend,
                'status': 'Completed',
            },
            'evaluation': {
                'technical_skills': 19,
                'problem_solving': 18,
                'code_quality': 18,
                'communication': 18,
                'teamwork': 19,
                'feedback': 'Demonstrated exemplary DevOps practices, robust automation scripts, and seamless collaboration across engineering teams.',
            },
        },
        {
            'intern_id': 'PSMI015',
            'full_name': 'Sneha Patel',
            'email': 'sneha.patel@problemsolvingmind.org',
            'domain': 'UI/UX Design & Frontend Engineering',
            'photo_filename': 'PSMI015.jpeg',
            'cert_id': 'PSM-CERT-PSMI015',
            'internship': {
                'start_date': date(2025, 10, 15),
                'end_date': date(2026, 4, 15),
                'duration_label': '15 October 2025 - 15 April 2026',
                'status': 'Completed',
                'organisation': 'Problem Solving Mind',
            },
            'project': {
                'title': 'Accessible Design System & Enterprise UI Library',
                'description': 'Design token architecture, WCAG 2.1 AA accessible React component library, and responsive design systems for public verification.',
                'technologies': 'React, TypeScript, Figma, Tailwind CSS, Storybook',
                'github_url': 'https://github.com/problemsolvingmind/enterprise-design-system',
                'live_url': frontend,
                'status': 'Completed',
            },
            'evaluation': {
                'technical_skills': 18,
                'problem_solving': 18,
                'code_quality': 19,
                'communication': 19,
                'teamwork': 18,
                'feedback': 'Remarkable attention to detail in UI/UX ergonomics, accessibility standards, and clean modular component design.',
            },
        },
    ]

    for item in seed_interns:
        intern = Intern.query.filter_by(intern_id=item['intern_id']).first()
        photo_path = str((upload_root / 'photos' / item['photo_filename']).resolve())

        if not intern:
            intern = Intern(
                intern_id=item['intern_id'],
                full_name=item['full_name'],
                email=item['email'],
                domain=item['domain'],
                photo_path=photo_path,
                mentor=mentor,
                is_active=True,
            )
            intern.internship = Internship(
                start_date=item['internship']['start_date'],
                end_date=item['internship']['end_date'],
                duration_label=item['internship']['duration_label'],
                status=item['internship']['status'],
                organisation=item['internship']['organisation'],
            )
            intern.project = Project(
                title=item['project']['title'],
                description=item['project']['description'],
                technologies=item['project']['technologies'],
                github_url=item['project']['github_url'],
                live_url=item['project']['live_url'],
                status=item['project']['status'],
            )
            eval_data = item['evaluation']
            intern.evaluation = MentorEvaluation(
                mentor=mentor,
                technical_skills=eval_data['technical_skills'],
                problem_solving=eval_data['problem_solving'],
                code_quality=eval_data['code_quality'],
                communication=eval_data['communication'],
                teamwork=eval_data['teamwork'],
                feedback=eval_data['feedback'],
                is_published=True,
            )
            intern.evaluation.calculate()
            db.session.add(intern)
            db.session.flush()
        else:
            intern.photo_path = photo_path
            intern.full_name = item['full_name']
            intern.domain = item['domain']

        cert_id = item['cert_id']
        payload = f"{frontend}/verify?id={cert_id}"
        certificate = Certificate.query.filter_by(certificate_id=cert_id).first()
        if not certificate:
            certificate = Certificate(
                intern=intern,
                certificate_id=cert_id,
                qr_payload=payload,
                status='Valid',
                issued_at=datetime.utcnow(),
            )

        qr_path = qr_dir / f"{cert_id}.png"
        pdf_path = cert_dir / f"{cert_id}.pdf"
        generate_qr_png(payload, qr_path)
        generate_certificate_pdf(certificate, intern, intern.internship, company, pdf_path, qr_path)

        certificate.qr_payload = payload
        certificate.qr_image_path = str(qr_path)
        certificate.pdf_path = str(pdf_path)
        db.session.add(certificate)

    db.session.commit()
    print('All 4 interns successfully seeded and certificates generated!')
