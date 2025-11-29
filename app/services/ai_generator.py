from app.schemas.ai_schemas import AIEmailRequest, AIEmailResponse


def generate_phishing_email(request: AIEmailRequest) -> AIEmailResponse:
    scenario = request.scenario.lower()
    tone = request.tone.lower()
    difficulty = request.difficulty.lower()
    
    # Base templates based on scenario
    scenarios = {
        "password_reset": {
            "subject": "Urgent: Password Reset Required",
            "body": """
            <html>
            <body>
            <p>Dear User,</p>
            <p>We detected unusual activity on your account. For your security, please reset your password immediately.</p>
            <p><a href="{click_url}">Click here to reset your password</a></p>
            <p>If you did not request this, please ignore this email.</p>
            <p>Best regards,<br>IT Security Team</p>
            </body>
            </html>
            """
        },
        "invoice": {
            "subject": "Payment Required - Invoice #{invoice_num}",
            "body": """
            <html>
            <body>
            <p>Hello,</p>
            <p>Your invoice is ready for review. Please make payment at your earliest convenience.</p>
            <p><a href="{click_url}">View Invoice</a></p>
            <p>Thank you,<br>Accounting Department</p>
            </body>
            </html>
            """
        },
        "package_delivery": {
            "subject": "Package Delivery Notification",
            "body": """
            <html>
            <body>
            <p>Hello,</p>
            <p>You have a package waiting for delivery. Please confirm your delivery address.</p>
            <p><a href="{click_url}">Track Package</a></p>
            <p>Best regards,<br>Delivery Service</p>
            </body>
            </html>
            """
        }
    }
    
    # Default scenario
    template = scenarios.get(scenario, scenarios["password_reset"])
    
    # Adjust based on tone
    if tone == "urgent":
        template["subject"] = "URGENT: " + template["subject"]
    elif tone == "friendly":
        template["body"] = template["body"].replace("Dear User", "Hi there!")
    
    # Adjust based on difficulty
    if difficulty == "easy":
        template["body"] = template["body"].replace("Click here", "CLICK HERE NOW")
    elif difficulty == "hard":
        template["body"] = template["body"].replace("Click here", "Review details")
    
    return AIEmailResponse(
        subject=template["subject"],
        body_html=template["body"]
    )

