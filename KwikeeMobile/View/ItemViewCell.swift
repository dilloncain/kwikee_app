//
//  ItemViewCell.swift
//  KwikeeMobile
//
//  Created by Dillon Cain on 1/7/19.
//  Copyright © 2019 Cain Computers. All rights reserved.
//

import UIKit

class ItemViewCell: UITableViewCell {

    @IBOutlet weak var lbItemName: UILabel!
    @IBOutlet weak var lbItemShortDescription: UILabel!
    @IBOutlet weak var lbItemPrice: UILabel!
    @IBOutlet weak var imgItemImage: UIImageView!
    
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
    }


}
