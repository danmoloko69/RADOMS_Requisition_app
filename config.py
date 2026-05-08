# ==========================================
# CONFIGURATION FILE
# ==========================================

# Blockchain Network Settings
SEPOLIA_RPC_URL = "https://ethereum-sepolia-rpc.publicnode.com"
CONTRACT_ADDRESS = "0x6D839599e21569268996Ed4828Ff7Be7c8885e70"

# Application Display Settings
APP_NAME = "RADOMS Requisition"
TAGLINE = "From Infestation to Protection"
DESCRIPTION = "A blockchain-powered platform solving the fragmentation and lack of trust in the fumigation industry."

# Path to the new logo image
LOGO_PATH = "RADOMS_Logo_New.png" 

# Human-Readable Status Mapping
STATUS_MAP = {
    0: "Requested",
    1: "Assigned",
    2: "Unassigned",
    3: "In Progress",
    4: "Completed",
    5: "Cancelled"
}

# Smart Contract ABI
CONTRACT_ABI = [
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_provider",
				"type": "address"
			}
		],
		"name": "approveProvider",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_requestId",
				"type": "uint256"
			}
		],
		"name": "cancelServiceRequest",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_requestId",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_serviceNotes",
				"type": "string"
			}
		],
		"name": "completeService",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_pestType",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_customerLocation",
				"type": "string"
			}
		],
		"name": "createServiceRequest",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_requestId",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "_provider",
				"type": "address"
			}
		],
		"name": "manuallyAssignProvider",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_location",
				"type": "string"
			}
		],
		"name": "registerCustomer",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "string",
				"name": "_companyName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_serviceLocation",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_certifications",
				"type": "string"
			}
		],
		"name": "registerProvider",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "requestId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "customer",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "ServiceCancelled",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "requestId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "provider",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "ServiceCompleted",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "requestId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "customer",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "pestType",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "ServiceRequested",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "requestId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "provider",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "ServiceStarted",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_requestId",
				"type": "uint256"
			}
		],
		"name": "startService",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "requestId",
				"type": "uint256"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "provider",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "timestamp",
				"type": "uint256"
			}
		],
		"name": "TechnicianAssigned",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "admin",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "customers",
		"outputs": [
			{
				"internalType": "address",
				"name": "customerAddress",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "location",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isRegistered",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_customer",
				"type": "address"
			}
		],
		"name": "getCustomerDetails",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "customerAddress",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "location",
						"type": "string"
					},
					{
						"internalType": "bool",
						"name": "isRegistered",
						"type": "bool"
					}
				],
				"internalType": "struct RADOMSRequisition.Customer",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "_provider",
				"type": "address"
			}
		],
		"name": "getProviderDetails",
		"outputs": [
			{
				"components": [
					{
						"internalType": "address",
						"name": "providerAddress",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "companyName",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "serviceLocation",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "certifications",
						"type": "string"
					},
					{
						"internalType": "bool",
						"name": "isApproved",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "isRegistered",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "isActive",
						"type": "bool"
					}
				],
				"internalType": "struct RADOMSRequisition.Provider",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_requestId",
				"type": "uint256"
			}
		],
		"name": "getRequestDetails",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint256",
						"name": "requestId",
						"type": "uint256"
					},
					{
						"internalType": "address",
						"name": "customer",
						"type": "address"
					},
					{
						"internalType": "string",
						"name": "pestType",
						"type": "string"
					},
					{
						"internalType": "string",
						"name": "customerLocation",
						"type": "string"
					},
					{
						"internalType": "address",
						"name": "assignedProvider",
						"type": "address"
					},
					{
						"internalType": "enum RADOMSRequisition.ServiceStatus",
						"name": "status",
						"type": "uint8"
					},
					{
						"internalType": "uint256",
						"name": "createdAt",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "startedAt",
						"type": "uint256"
					},
					{
						"internalType": "uint256",
						"name": "completedAt",
						"type": "uint256"
					},
					{
						"internalType": "string",
						"name": "serviceNotes",
						"type": "string"
					}
				],
				"internalType": "struct RADOMSRequisition.ServiceRequest",
				"name": "",
				"type": "tuple"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "nextRequestId",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "providers",
		"outputs": [
			{
				"internalType": "address",
				"name": "providerAddress",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "companyName",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "serviceLocation",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "certifications",
				"type": "string"
			},
			{
				"internalType": "bool",
				"name": "isApproved",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "isRegistered",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "isActive",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "serviceRequests",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "requestId",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "customer",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "pestType",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "customerLocation",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "assignedProvider",
				"type": "address"
			},
			{
				"internalType": "enum RADOMSRequisition.ServiceStatus",
				"name": "status",
				"type": "uint8"
			},
			{
				"internalType": "uint256",
				"name": "createdAt",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "startedAt",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "completedAt",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "serviceNotes",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
