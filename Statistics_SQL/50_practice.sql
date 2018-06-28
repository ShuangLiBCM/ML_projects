USE Northwind
-- 5.
-- SELECT OrderID, OrderDate FROM Orders
-- WHERE EmployeeID = 5;

-- 7
-- SELECT ProductID, ProductName FROM Products
-- WHERE ProductName LIKE '%Queso%';

-- 8
-- "Pay attention to the use of = and or"
-- SELECT OrderID, CustomerID, ShipCountry FROM Orders
-- WHERE ShipCountry = 'France' or 'Belgium';

-- 9
-- SELECT OrderID, CustomerID, ShipCountry FROM Orders
-- WHERE ShipCountry in ('Brazil', 'Mexico');

-- 10
-- SELECT FirstName, LastName, Title, BirthDate
-- FROM Employees
-- ORDER BY BirthDate;

-- 11
-- SELECT FirstName, LastName, Title, DATE(BirthDate)
-- FROM Employees
-- ORDER BY BirthDate;

-- 12
-- "Pay attention to the use of CONCAT"
-- SELECT FirstName, LastName,
-- CONCAT(FirstName, ' ', LastName) As FullName
-- FROM Employees;

-- 13
-- "Pay attention to the use or arithmatic operator"
-- SELECT UnitPrice, Quantity,
-- UnitPrice * Quantity AS TotalPrice
-- FROM OrderDetails;

-- 14
-- SELECT  COUNT(CustomerID) AS TotalCustomers
-- FROM Customers;

-- 15
-- "Pay attention to the Min"
-- SELECT Min(OrderDate) AS FirstOrder
-- FROM Orders;
-- "Pay attention to the use of LIMIT"
-- SELECT OrderDate AS FirstOrder
-- FROM Orders
-- ORDER BY OrderDate
-- LIMIT 1;

-- 16
-- SELECT Country FROM Customers
-- GROUP BY Country;

-- 17
-- SELECT ContactTitle, Count(ContactTitle) AS Occurence
-- FROM Customers
-- GROUP BY ContactTitle;

-- 18
-- "Pay attention to the two different syntax"
-- SELECT ProductID, ProductName, CompanyName AS Supplier
-- FROM Products, Suppliers
-- WHERE Products.SupplierID = Suppliers.SupplierID;

-- SELECT ProductID, ProductName, CompanyName AS Supplier
-- FROM Products JOIN Suppliers
-- ON Products.SupplierID = Suppliers.SupplierID;

-- 19
-- SELECT OrderID, DATE(OrderDate), CompanyName AS Shipper
-- FROM Orders JOIN Shippers
-- ON Orders.ShipVia = Shippers.ShipperID
-- ORDER BY OrderID
-- LIMIT 3;

-- 20
-- SELECT CategoryName, COUNT(CategoryName) AS Count
-- FROM Categories JOIN Products
-- ON Categories.CategoryID = Products.CategoryID
-- GROUP BY CategoryName
-- ORDER BY Count
-- DESC;

-- 21
-- SELECT Country, City, COUNT(CustomerID) AS TotalCustomers
-- FROM Customers
-- GROUP BY Country, City
-- ORDER BY TotalCustomers
-- DESC;

-- 22
-- SELECT ProductID, ProductName, UnitsInStock, ReorderLevel
-- FROM Products
-- WHERE UnitsInStock < ReorderLevel
-- ORDER BY ProductID;

-- 23
-- SELECT ProductID, ProductName, UnitsInStock, ReorderLevel
-- FROM Products
-- WHERE (UnitsInStock + UnitsOnOrder  <= ReorderLevel)
-- and (!Discontinued)
-- ORDER BY ProductID;

-- ** 24
-- "Pay attention to the use of case, end"
-- SELECT CustomerID, CompanyName, Region
-- FROM Customers
-- ORDER BY
--   Case
    -- when Region is null then 1
--     else 0
--   End,
--   Region, CustomerID;

-- 25
-- "Pay attention to the use of DECIMAL"
-- SELECT ShipCountry, CAST(AVG(Freight) AS DECIMAL(10, 2)) AS average_freight
-- FROM Orders
-- GROUP BY ShipCountry
-- ORDER BY average_freight
-- DESC
-- LIMIT 3;

-- 26
-- SELECT ShipCountry, CAST(AVG(Freight) AS DECIMAL(10, 2)) AS average_freight
-- FROM Orders
-- WHERE OrderDate LIKE '%2015%'
-- GROUP BY ShipCountry
-- ORDER BY average_freight
-- DESC
-- LIMIT 3;

-- 27
-- "BETWEEN AND does not include the first item"
-- SELECT ShipCountry, CAST(AVG(Freight) AS DECIMAL(10, 2)) AS average_freight
-- FROM Orders
-- WHERE OrderDate BETWEEN '2014/12/31' AND '2015/12/31'
-- GROUP BY ShipCountry
-- ORDER BY average_freight
-- DESC;

-- 28
-- "BETWEEN AND does not include the first item"
-- "Wrong answer"
-- SELECT ShipCountry, CAST(AVG(Freight) AS DECIMAL(10, 2)) AS average_freight
-- FROM Orders
-- WHERE DATEDIFF(month, OrderDate, SELECT max(DATE(OrderDate)) FROM Orders) <= 12
-- GROUP BY ShipCountry
-- ORDER BY average_freight
-- DESC;

-- 29
-- "After Join, Use tablename.column name to avoid ambiguity"
-- SELECT Employees.EmployeeID, Employees.LastName, Orders.OrderID,
-- Products.ProductName, OrderDetails.Quantity
-- FROM Employees
-- JOIN Orders ON Employees.EmployeeID = Orders.EmployeeID
-- JOIN OrderDetails ON Orders.OrderID = OrderDetails.OrderID
-- JOIN Products ON OrderDetails.ProductID = Products.ProductID
-- ORDER BY Orders.OrderID, Products.ProductID

-- 30
-- "Again, when joining table, use tablename.column to avoid ambiguity"
-- "If using JOIN, and select NULL in Orders.CustomerID, nothing will appear"
-- SELECT Customers.CustomerID, Orders.CustomerID
-- FROM Customers
-- Left JOIN Orders
-- ON Orders.CustomerID = Customers.CustomerID
-- WHERE Orders.CustomerID is null

-- *31
-- "Pay attention to the use of left join and Selection of table content before join"
SELECT Customers.CustomerID, Orders.CustomerID
FROM Customers
Left JOIN Orders
ON Customers.CustomerID = Orders.CustomerID
and Orders.EmployeeID = 4
WHERE Orders.EmployeeID is null
