//
//  PaymentViewController.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 12/30/18.
//  Copyright © 2018 Cain Computers. All rights reserved.
//

import UIKit
import Stripe

class PaymentViewController: UIViewController {

    @IBOutlet var cardTextField: STPPaymentCardTextField!
    override func viewDidLoad() {
        super.viewDidLoad()

    }
    @IBAction func placeOrder(_ sender: Any) {
        
        APIManager.shared.getLatestOrder { (json) in
            
            if json["order"]["status"] != nil || json["order"]["status"] == "Delivered" {
                // Processing the payment and creates an order
                
                let card = self.cardTextField.cardParams
                
                STPAPIClient.shared().createToken(withCard: card, completion: { (token, error) in
                    
                    if let myError = error {
                        print("Error:", myError)
                    } else if let stripeToken = token {
                        
                        APIManager.shared.createOrder(stripeToken: stripeToken.tokenId, completionHandler: { (json) in
                            Cart.currentCart.reset()
                            self.performSegue(withIdentifier: "ViewOrder", sender: self)
                        })
                    }
                })
                
            } else {
                // Showing an alert message
                
                let cancelAction = UIAlertAction(title: "OK", style: .cancel)
                let okAction = UIAlertAction(title: "Go to order", style: .default, handler: { (action) in
                    self.performSegue(withIdentifier: "ViewOrder", sender: self)
                })
                
                let alertView = UIAlertController(title: "Already ordered?", message: "Your current order isn't completed", preferredStyle: .alert)
                
                alertView.addAction(okAction)
                alertView.addAction(cancelAction)
                
                self.present(alertView, animated: true, completion: nil)
            }
        }
    }
    
}
