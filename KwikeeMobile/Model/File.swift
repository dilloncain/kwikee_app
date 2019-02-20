//
//  File.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 1/8/19.
//  Copyright © 2019 Cain Computers. All rights reserved.
//

import Foundation

class CartItem {
    
    var item: Item
    var qty: Int
    
    init(item: Item, qty: Int) {
        self.item = item
        self.qty = qty
    }
}

class Cart {
    
    static let currentCart = Cart()
    
    var business: Business?   // ? for possible nil
    var items = [CartItem]()
    var address: String?
    
    func getTotal() -> Float {
        var total: Float = 0
        
        for item in self.items {
            total = total + Float(item.qty) * item.item.price!
            
        }
        
        return total
    }
    
    func reset() {
        self.business = nil
        self.items = []
        self.address = nil
    }
}
