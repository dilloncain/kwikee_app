//
//  Item.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 1/7/19.
//  Copyright © 2019 Cain Computers. All rights reserved.
//

import Foundation
import SwiftyJSON

class Item {
    
    var id: Int?
    var name: String?
    var short_description: String?
    var image: String?
    var price: Float?
    
    init(json: JSON) {
        
        self.id = json["id"].int
        self.name = json["name"].string
        self.short_description = json["short_description"].string
        self.image = json["image"].string
        self.price = json["price"].float
        
    }
}
