//
//  APIManager.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 12/31/18.
//  Copyright © 2018 Cain Computers. All rights reserved.
//

import Foundation
import Alamofire
import SwiftyJSON
import FBSDKLoginKit


class APIManager {
    
    static let shared = APIManager()
    
    let baseURL = NSURL(string: BASE_URL)
    
    var accessToken = ""
    var refreshToken = ""
    var expired = Date()    // Date <-------- Not data!
    
    // API to login a user
    func login(userType: String, completionHandler: @escaping (NSError?) -> Void) {         // Closure RESTful API
        
        let path = "api/social/convert-token/"
        let url = baseURL!.appendingPathComponent(path)
        let params: [String: Any] = [
            "grant_type": "convert_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "backend": "facebook",
            "token": FBSDKAccessToken.current().tokenString,
            "user_type": userType
        ]
        
            AF.request(url!, method: .post, parameters: params, encoding: JSONEncoding.default, headers: nil).responseJSON { (response) in
            switch response.result{
            case .success(let value):
                let jsonData = JSON(value)
                self.accessToken = jsonData["access_token"].string!
                self.refreshToken = jsonData["refresh_token"].string!
                self.expired = Date().addingTimeInterval(TimeInterval(jsonData["expires_in"].int!))
                
                completionHandler(nil)
                break
                
            case .failure(let error):
                completionHandler(error as NSError?)
                break
            }
        }
    }
    // API to log a user out
    func logout(completionHandler: @ escaping (NSError?) -> Void) {
        
        let path = "api/social/revoke-token/"
        let url = baseURL!.appendingPathComponent(path)
        let params: [String: Any] = [
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "token": self.accessToken
        ]
        
        AF.request(url!, method: .post, parameters: params, encoding: JSONEncoding.default, headers: nil).responseString { (response) in
            
            switch response.result{
            case .success:
                completionHandler(nil)
                break
            case .failure(let error):
                completionHandler(error as NSError?)
                break
            }
        }
    }
    
    // API to refresh the token when it's expired
    func refreshTokenIfNeed(completionHandler: @escaping () -> Void) {
        
        let path = "api/social/refresh-token/"
        let url = baseURL?.appendingPathComponent(path)
        let params: [String: Any] = [
            "access_token" : self.accessToken,
            "refresh_token": self.refreshToken
        ]
        
        if (Date() > self.expired) {
            AF.request(url!, method: .post, parameters: params, encoding: URLEncoding(), headers: nil).responseJSON(completionHandler: { (response) in
                    
                switch response.result{
                case .success(let value):
                    let jsonData = JSON(value)
                    self.accessToken = jsonData["access_token"].string!
                    self.expired = Date().addingTimeInterval(TimeInterval(jsonData["expires_in"].int!))
                    completionHandler()
                    break
                    
                case .failure:
                    break
                }
            })
        } else {
            completionHandler()
        }
    }
    
    // Request Server Function
    func requestServer(_ method: HTTPMethod,_ path: String,_ params: [String: Any]?,_ encoding: ParameterEncoding,_ completionHandler: @escaping (JSON) -> Void) {
        
        let url = baseURL?.appendingPathComponent(path)
        
        refreshTokenIfNeed {
            
            AF.request(url!, method: method, parameters: params, encoding: encoding, headers: nil).responseJSON{ response in
                
                switch response.result {
                case .success(let value):
                    let jsonData = JSON(value)
                    completionHandler(jsonData)
                    break
                    
                case .failure:
                    //completionHandler(nil)
                    break
                }
            }
        }
        
    }
    
    // API getting Business list
    func getBusinesses(completionHandler: @escaping (JSON?) -> Void) {
        
        let path = "api/customer/businesses/"
        requestServer(.get, path, nil, URLEncoding(), completionHandler)
        
    }
    
    
    // API - Getting list of items of a Business.
    func getItems(businessId: Int, completionHandler: @escaping (JSON) -> Void) {
        
        let path = "api/customer/items/\(businessId)"
        requestServer(.get, path, nil, URLEncoding(), completionHandler)
        
    }

    // API - Creating new order
    
    func createOrder(stripeToken: String, completionHandler: @escaping (JSON) -> Void) {
        
        let path = "api/customer/order/add/"
        let simpleArray = Cart.currentCart.items
        let jsonArray = simpleArray.map { item in
            return [
                "item_id": item.item.id!,
                "quantity": item.qty
            ]
        }
        
        if JSONSerialization.isValidJSONObject(jsonArray) {
            
            do {
                
                let data = try JSONSerialization.data(withJSONObject: jsonArray, options: [])
                let dataString = NSString(data: data, encoding: String.Encoding.utf8.rawValue)
                
                let params: [String: Any] = [
                    "access_token": self.accessToken,
                    "stripe_token": stripeToken,
                    "business_id": "\(Cart.currentCart.business!.id!)",
                    "order_details": dataString,
                    "address": Cart.currentCart.address!
                ]
                
                requestServer(.post, path, params, URLEncoding(), completionHandler)
                
            }
            catch {
                print("JSON serialization failed: \(error)")
            }
        }
    }
    
    // API - Getting the latest order (Customer)
    func getLatestOrder(completionHandler: @escaping (JSON) -> Void) {
        
        let path = "api/customer/order/latest/"
        let params: [String: Any] = [
            "access_token": self.accessToken
        ]
        
        requestServer(.get, path, params, URLEncoding(), completionHandler)
    }
    
    
    
    
    
    
}


