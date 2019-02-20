//
//  ItemDetailsViewController.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 12/30/18.
//  Copyright © 2018 Cain Computers. All rights reserved.
//

import UIKit

class ItemDetailsViewController: UIViewController {

    @IBOutlet weak var imgItem: UIImageView!
    @IBOutlet weak var lbItemName: UILabel!
    @IBOutlet weak var lbItemShortDescription: UILabel!
    
    
    @IBOutlet weak var lbTotal: UILabel!
    @IBOutlet weak var lbQty: UILabel!
    
    var item: Item?
    var business: Business?
    var qty = 1
    
    override func viewDidLoad() {
        super.viewDidLoad()
        loadItem()

    }
    
    func loadItem() {
        
        if let price = item?.price {
            lbTotal.text = "$\(price)"
        }
        
        lbItemName.text = item?.name
        lbItemShortDescription.text = item?.short_description
        
        if let imageUrl = item?.image {
            Helpers.loadImage(imgItem, "\(imageUrl)")
        }
    }
  
    @IBAction func addToCart(_ sender: Any) {
        
        let image = UIImageView(frame: CGRect(x: 0, y: 0, width: 60, height: 40))
        image.image = UIImage(named: "button_chicken")
        image.center = CGPoint(x: self.view.frame.width/2, y: self.view.frame.height-100)
        self.view.addSubview(image)
        
        UIView.animate(withDuration: 1.0, delay: 0.0, options: UIView.AnimationOptions.curveEaseOut, animations: { image.center = CGPoint(x: self.view.frame.width - 40, y: 24) }, completion: { _ in image.removeFromSuperview()
            
            let cartItem = CartItem(item: self.item!, qty: self.qty)
            
            guard let cartBusiness = Cart.currentCart.business, let currentBusiness = self.business else {
                // If those requirements are not met run below
                Cart.currentCart.business = self.business
                Cart.currentCart.items.append(cartItem)
                return
            }
            
            let cancelAction = UIAlertAction(title: "Cancel", style: .cancel)
            
            // If ordering item from the same business
            if cartBusiness.id == currentBusiness.id {
                
                let inCart = Cart.currentCart.items.index(where: { (item) -> Bool in
                    
                    return item.item.id! == cartItem.item.id!
                })
                
                if let index = inCart {
                    
                    let alertView = UIAlertController(title: "Add more?", message: "Your cart already has this item. Do you want to add more?", preferredStyle: .alert)
                    
                    let okAction = UIAlertAction(title: "Add more", style: .default, handler: { (action: UIAlertAction!) in
                    
                        Cart.currentCart.items[index].qty += self.qty
                    })
                    
                    alertView.addAction(okAction)
                    alertView.addAction(cancelAction)
                    
                    self.present(alertView, animated: true, completion: nil)
                } else {
                    Cart.currentCart.items.append(cartItem)
                }
                
            }
            else { // If ordering item from another business
                
                let alertView = UIAlertController(title: "Start new cart?", message: "You're ordering an item from another business. Would you like to clear the current cart?", preferredStyle: .alert)
                
                let okAction = UIAlertAction(title: "New Cart", style: .default, handler: { (action: UIAlertAction!) in
                    
                    Cart.currentCart.items = []
                    Cart.currentCart.items.append(cartItem)
                    Cart.currentCart.business = self.business
                })
                
                alertView.addAction(okAction)
                alertView.addAction(cancelAction)
                
                self.present(alertView, animated: true, completion: nil)
            }
            
        })
    }
    
    @IBAction func removeQty(_ sender: Any) {
        
        if qty >= 2 {
            qty -= 1
            lbQty.text = String(qty)
            
            if let price = item?.price {
                lbTotal.text = "$\(price * Float(qty))"
            }
        }
    }
    
    @IBAction func addQty(_ sender: Any) {
        
        if qty < 99 {
            qty += 1
            lbQty.text = String(qty)
            
            if let price = item?.price {
                lbTotal.text = "$\(price * Float(qty))"
            }
        }
    }
    
}
