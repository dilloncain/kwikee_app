//
//  BusinessViewController.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 12/30/18.
//  Copyright © 2018 Cain Computers. All rights reserved.
//

import UIKit

class BusinessViewController: UIViewController {

    @IBOutlet var menuBarButton: UIBarButtonItem!
    @IBOutlet weak var searchBusiness: UISearchBar!
    @IBOutlet weak var tbvBusiness: UITableView!

    
    var businesses = [Business]()
    var filteredBusinesses = [Business]()   // Filters results
    
    let activityIndicator = UIActivityIndicatorView()
    
    override func viewDidLoad() {
        super.viewDidLoad()

        if self.revealViewController() != nil {
            
        
            menuBarButton.target = self.revealViewController()
            menuBarButton.action = #selector(SWRevealViewController.revealToggle(_:))
            self.view.addGestureRecognizer(self.revealViewController().panGestureRecognizer())
        }
        
        loadBusinesses()
    }
    
    func loadBusinesses() {
        
        Helpers.showActivityIndicator(activityIndicator, view)
        
        APIManager.shared.getBusinesses { (json) in
            
            if json != nil {
                
                self.businesses = []
                if let listBus = json?["businesses"].array {
                    for item in listBus {
                        let business = Business(json: item)
                        self.businesses.append(business)
                    }
                    
                    self.tbvBusiness.reloadData()
                    Helpers.hideActivityIndicator(self.activityIndicator)
                }
            }
        }
    }

    
    
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        
        if segue.identifier == "ItemList" {
            
            let controller = segue.destination as! ItemListTableViewController
            controller.business = businesses[(tbvBusiness.indexPathForSelectedRow?.row)!]
        }
    }
    
}

extension BusinessViewController: UISearchBarDelegate {
    
    func searchBar(_ searchBar: UISearchBar, textDidChange searchText: String) {
        
        filteredBusinesses = self.businesses.filter({ (res: Business) -> Bool in
            
            return res.name?.lowercased().range(of: searchText.lowercased()) != nil
        })
        
        self.tbvBusiness.reloadData()
    }
}

extension BusinessViewController: UITableViewDelegate, UITableViewDataSource {
    
    func numberOfSections(in tableView: UITableView) -> Int {
        return 1
    }
    
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        
        if searchBusiness.text != "" {
            return self.filteredBusinesses.count
        }
        
        return self.businesses.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "BusinessCell", for: indexPath) as! BusinessViewCell
        
        let business: Business
        
        if searchBusiness.text != "" {
            business = filteredBusinesses[indexPath.row]
        } else {
            business = businesses[indexPath.row]
        }
        
        cell.lbBusinessName.text = business.name!
        cell.lbBusinessAddress.text = business.address!
        
        if let logoName = business.logo {
            Helpers.loadImage(cell.imgBusinessLogo, "\(logoName)")
        }
        
        return cell
    }
}
