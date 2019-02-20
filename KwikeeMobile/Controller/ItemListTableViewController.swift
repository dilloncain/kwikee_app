//
//  ItemListTableViewController.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 12/30/18.
//  Copyright © 2018 Cain Computers. All rights reserved.
//

import UIKit

class ItemListTableViewController: UITableViewController {

    var business: Business?
    var items = [Item]()
    
    let activityIndicator = UIActivityIndicatorView()

    
    override func viewDidLoad() {
        super.viewDidLoad()
        
        if let businessName = business?.name {
            self.navigationItem.title = businessName
        }

        loadItems()
        
    }
    
    func loadItems() {
        
        Helpers.showActivityIndicator(activityIndicator, view)
        
        if let businessId = business?.id {
            
            APIManager.shared.getItems(businessId: businessId) { (json) in
                
                if json != nil {
                    self.items = []
                    
                    if let tempItems = json["items"].array {
                        
                        for item in tempItems {
                            let item = Item(json: item)
                            self.items.append(item)
                        }
                        self.tableView.reloadData()
                        Helpers.hideActivityIndicator(self.activityIndicator)

                    }
                }
            }
        }
    }
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        
        if segue.identifier == "ItemDetails" {
            let controller = segue.destination as! ItemDetailsViewController
            controller.item = items[((tableView.indexPathForSelectedRow?.row)!)]
            controller.business = business
        }
    }

    override func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    override func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return items.count
    }
    
    override func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "ItemCell", for: indexPath) as! ItemViewCell
        
        let item = items[indexPath.row]
        cell.lbItemName.text = item.name
        cell.lbItemShortDescription.text = item.short_description
        
        if let price = item.price {
            cell.lbItemPrice.text = "$\(price)"
        }
        
        if let image = item.image {
            Helpers.loadImage(cell.imgItemImage, "\(image)")
            
        }
        
        return cell
    }
    
}
