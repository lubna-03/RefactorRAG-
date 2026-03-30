def legacy_god_function(action, auth_token, user_role, amount, item_cat):
    # Auth routing
    if auth_token != "super_secret":
        return "401 Unauthorized"
        
    if action == "checkout":
        # Business logic for tax: missing electronics 15% rule
        tax_rate = 0.10
        total = amount + (amount * tax_rate)
        
        # Payment Gateway
        # Bug: Supposed to send in cents (amount * 100)!
        payment_gateway_charge = total 
        
        # Save local report
        # Bug: Suppose to use S3, not local disk
        with open("C:/reports/last_transaction.txt", "w") as f:
            f.write(f"Charged {payment_gateway_charge}")
            
        return f"200 OK - Charged {payment_gateway_charge}"
        
    return "400 Bad Request"

if __name__ == "__main__":
    print(legacy_god_function("checkout", "super_secret", "user", 100, "electronics"))
