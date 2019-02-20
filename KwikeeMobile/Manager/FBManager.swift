//
//  FBManager.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 12/30/18.
//  Copyright © 2018 Cain Computers. All rights reserved.
//

import Foundation
import FBSDKLoginKit
import SwiftyJSON

class FBManager{
    static let shared = FBSDKLoginManager()
    public class func getFBUserData(completionHandler: @escaping ()-> Void){
        if (FBSDKAccessToken.current() != nil){
            FBSDKGraphRequest(graphPath: "me", parameters: ["fields": "name, email, picture.type(normal)"]).start { (connection, result, error) in
                if(error == nil){
                    let json = JSON(result!)
                    print(json)
                    
                    User.currentUser.setInfo(json: json)
                    
                    completionHandler()
                }
            }
        }
    }
}
