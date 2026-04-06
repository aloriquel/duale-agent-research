from src.search_service import SearchService
from src.report_generator import ReportGenerator
from src.email_service import EmailService
import datetime

def main():
    print(f"--- Duale Research Agent Staring: {datetime.datetime.now()} ---")
    
    # 1. Search
    search_service = SearchService()
    results = search_service.perform_search()
    
    # 2. Generate Report
    generator = ReportGenerator()
    report_html = generator.generate_report(results)
    
    # 3. Generate LinkedIn Post
    print("Generating LinkedIn Newsletter post...")
    linkedin_post = generator.generate_linkedin_post(results)
    
    # Save LinkedIn post to file so the user can copy it
    with open("linkedin_post.txt", "w", encoding="utf-8") as f:
        f.write(linkedin_post)
    print("LinkedIn post saved to 'linkedin_post.txt'.")
    
    # 4. Send Email
    email_service = EmailService()
    today = datetime.date.today().strftime("%d/%m/%Y")
    subject = f"Informe Semanal de Mercado Duale - {today}"
    
    success = email_service.send_email(subject, report_html)
    
    if success:
        print("Workflow completed successfully.")
    else:
        print("Workflow failed at email stage.")

if __name__ == "__main__":
    main()
