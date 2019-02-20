//
//  Business.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 1/6/19.
//  Copyright © 2019 Cain Computers. All rights reserved.
//

import Foundation
import SwiftyJSON

class Business {
    
    var id: Int?
    var name: String?
    //var phone: String?
    var address: String?
    var logo: String?
    
    init(json: JSON) {
        self.id = json["id"].int
        self.name = json["name"].string
        //self.phone = json["phone"].string
        self.address = json["address"].string
        self.logo = json["logo"].string
        
        
    }
}
